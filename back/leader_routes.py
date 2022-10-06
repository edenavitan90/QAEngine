from flask import Flask, request, make_response, jsonify
from concurrent.futures import ThreadPoolExecutor
from pymongo import MongoClient
import concurrent.futures
import requests
import json
import time
import sys
import os

sys.path.insert(0, os.getcwd())
import consts

app = Flask(__name__)
le = None
PORT = None


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
def call_worker_get_qa_query(term, worker, shard_address):
    body = {"term": term, "worker": {"worker_name": worker[0], "address": worker[1], "job": worker[2],
                                     "status": worker[3]}, "shard_address": shard_address}
    worker_name = worker[0]
    worker_address = worker[1]
    url = f"http://{worker_address}/get_qa_query"
    headers = {'Content-type': 'application/json; charset=utf-8', 'Accept': 'text/json',
               'Sender-Domain': f"localhost:{PORT}"}
    response = requests.post(url=url, json=json.dumps(body), headers=headers)

    le.zk.set(f"{consts.BASE_PATH}/{worker_name}", f"{worker_address},{consts.WORKER},{consts.FREE}".encode())

    return response.json()


@app.route("/hello", methods=['GET'])
def hello():
    return "Hello World"


@app.route("/add_qa", methods=['POST'])
def add_qa():
    workers = get_workers(le.zk, consts.BASE_PATH)
    num_of_workers = len(workers)
    if num_of_workers == 0:
        # No available worker to handle the request.
        msg = "No available worker to handle the request."
        return make_response(jsonify(msg), 500)
    else:
        body = json.loads(request.json)
        question = body["question"]
        answer = body["answer"]
        qa = {"Question": question, "Answers": [{"Answer": answer, "Likes": 0, "Dislikes": 0}]}
        # set 2 min to timeout.
        t_end = time.time() + consts.TIMEOUT_2_MIN
        while time.time() < t_end:
            worker = get_free_worker(le.zk, consts.BASE_PATH)
            if worker is not None:
                worker_name = worker[0]
                worker_address = worker[1]

                le.zk.set(f"{consts.BASE_PATH}/{worker_name}",
                          f"{worker_address},{consts.WORKER},{consts.BUSY}".encode())
                worker = (worker_name, worker_address, consts.WORKER, consts.BUSY)

                url = f"http://{worker_address}/add_qa"
                new_body = {"qa": qa, "worker": worker}
                response = requests.post(url=url, json=json.dumps(new_body))
                le.zk.set(f"{consts.BASE_PATH}/{worker_name}",
                          f"{worker_address},{consts.WORKER},{consts.FREE}".encode())
                return make_response(jsonify(response.content.decode()), response.status_code)

        msg = "Error"
        return make_response(jsonify(msg), 500)


@app.route("/get_qa_query", methods=['GET'])
def get_qa_query():
    start = time.process_time()
    term = request.args.get('term')
    qa = []

    workers = get_workers(le.zk, consts.BASE_PATH)
    num_of_workers = len(workers)
    if num_of_workers == 0:
        # No available worker to handle the request.
        msg = "No available worker to handle the request."
        return make_response(jsonify(msg), 500)
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

                    futures.append(
                        executor.submit(call_worker_get_qa_query, term, worker, consts.SHARDS_ADDRESS[counter]))
                    counter += 1
                    num_of_request -= 1

            for future in concurrent.futures.as_completed(futures):
                qa.extend(future.result())

        qa_temp = []
        qa_final = []
        for i in qa:
            if i[1] != 0:
                qa_temp.append(i)

        qa_temp.sort(reverse=True, key=lambda y: y[1])

        for i in qa_temp:
            qa_final.append(i[0])

        end = time.process_time()
        print(f"process time: /get_qa_query [GET] - {'{:0.5f}'.format(end - start)} [SEC]")
        return qa_final[:10]
    return None


@app.route('/login', methods=['POST'])
def login():
    info = json.loads(request.json)
    username = info.get('username')
    password = info.get('password')

    uri = f"mongodb://{consts.MONGO_DB_MAIN_SERVER['primary']}"
    client = MongoClient(uri)
    db = client[consts.DB_NAME]
    users_collection = db[consts.USERS_COLLECTION]

    user = users_collection.find_one({"user_name": username}, {"_id": 0})
    if user is not None:
        if user["user_name"] == username and user["user_password"] == password:
            msg = "Login success."
            return make_response(jsonify(msg), 200)
        else:
            msg = "Login failed."
            return make_response(jsonify(msg), 401)
    else:
        msg = "Login failed."
        return make_response(jsonify(msg), 401)


@app.route('/register', methods=['POST'])
def register():
    info = json.loads(request.json)
    username = info.get('username')
    password = info.get('password')
    new_user = {"user_name": username, "user_password": password}

    uri = f"mongodb://{consts.MONGO_DB_MAIN_SERVER['primary']}"
    client = MongoClient(uri)
    db = client[consts.DB_NAME]
    users_collection = db[consts.USERS_COLLECTION]

    is_exists_user = users_collection.find_one({"user_name": username}, {"_id": 0})
    if is_exists_user is None:
        insert_result = users_collection.insert_one(new_user)
        if insert_result.inserted_id is not None:
            msg = "Registration success."
            return make_response(jsonify(msg), 201)
        else:
            msg = "Registration failed."
            return make_response(jsonify(msg), 501)
    else:
        msg = "Registration failed (user is already exists)."
        return make_response(jsonify(msg), 409)


@app.route('/update_question_rank', methods=['POST'])
def update_question_rank():
    workers = get_workers(le.zk, consts.BASE_PATH)
    num_of_workers = len(workers)
    if num_of_workers == 0:
        # No available worker to handle the request.
        msg = "No available worker to handle the request."
        return make_response(jsonify(msg), 500)
    else:
        body = json.loads(request.json)
        type = body.get('type')
        qa_id = body.get('qa_id')
        answer = body.get('answer')

        # set 2 min to timeout.
        t_end = time.time() + consts.TIMEOUT_2_MIN
        while time.time() < t_end:
            worker = get_free_worker(le.zk, consts.BASE_PATH)
            if worker is not None:
                worker_name = worker[0]
                worker_address = worker[1]

                le.zk.set(f"{consts.BASE_PATH}/{worker_name}",
                          f"{worker_address},{consts.WORKER},{consts.BUSY}".encode())
                worker = (worker_name, worker_address, consts.WORKER, consts.BUSY)

                url = f"http://{worker_address}/update_question_rank"
                new_body = {"qa_id": qa_id, "answer": answer, "type": type, "worker": worker}
                response = requests.post(url=url, json=json.dumps(new_body))
                le.zk.set(f"{consts.BASE_PATH}/{worker_name}",
                          f"{worker_address},{consts.WORKER},{consts.FREE}".encode())
                return make_response(jsonify(response.content.decode()), response.status_code)


def run(l_e, port):
    global le, PORT
    print("leader: run...")
    le = l_e
    PORT = port
    app.run(port=PORT, debug=True, use_reloader=False)
