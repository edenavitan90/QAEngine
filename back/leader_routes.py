import time
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, request
import concurrent.futures
import requests
import json
import sys
import os

sys.path.insert(0, os.getcwd())
import consts

app = Flask(__name__)
le = None


def get_workers(zk, path):
    children = zk.get_children(path)
    workers = []
    for child in children:
        address, job, status = zk.get(f"{path}/{child}")[0].decode().split(",")
        if job == consts.WORKER:
            workers.append((child, address, status))
    return workers


def get_free_worker(zk, path):
    workers = get_workers(le.zk, consts.BASE_PATH)
    for worker in workers:
        worker_name = worker[0]
        address, job, status = zk.get(f"{path}/{worker_name}")[0].decode().split(",")
        if status == consts.FREE:
            return worker_name, address, job, status
    return None


# Thread function.
def call_worker(term, worker, shard_address):
    body = {"term": term, "worker": {"worker_name": worker[0], "address": worker[1], "job": worker[2],
                                     "status": worker[3]}, "shard_address": shard_address}
    worker_name = worker[0]
    worker_address = worker[1]
    url = f"http://{worker_address}/get_qa_query"
    headers = {'Content-type': 'application/json; charset=utf-8', 'Accept': 'text/json'}
    response = requests.post(url=url, json=json.dumps(body), headers=headers)

    le.zk.set(f"{consts.BASE_PATH}/{worker_name}", f"{worker_address},{consts.WORKER},{consts.FREE}".encode())

    return response.json()


@app.route("/get_qa_query", methods=['GET'])
def get_qa_query():
    term = request.args.get('term')
    workers = get_workers(le.zk, consts.BASE_PATH)
    num_of_workers = len(workers)
    qa = []

    if num_of_workers == 0:
        # No available worker to handle the request.
        return None
    else:
        futures = []
        num_of_request = consts.NUMBER_OF_SHARD
        counter = 0
        with ThreadPoolExecutor(max_workers=consts.NUMBER_OF_SHARD) as executor:
            while True:
                if num_of_request <= 0:
                    break

                worker = get_free_worker(le.zk, consts.BASE_PATH)
                if worker is not None:
                    worker_name = worker[0]
                    worker_address = worker[1]

                    le.zk.set(f"{consts.BASE_PATH}/{worker_name}",
                              f"{worker_address},{consts.WORKER},{consts.BUSY}".encode())
                    worker = (worker_name, worker_address, consts.WORKER, consts.BUSY)

                    futures.append(executor.submit(call_worker, term, worker, consts.SHARDS_ADDRESS[counter]))
                    counter += 1
                    num_of_request -= 1

            for future in concurrent.futures.as_completed(futures):
                qa.extend(future.result())
                print(future)

        return qa
    return None


def run(l_e, port):
    global le
    print("leader: run...")
    le = l_e
    app.run(port=port, debug=True, use_reloader=False)
