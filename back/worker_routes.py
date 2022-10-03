from flask import Flask, request, make_response, jsonify
from pymongo import MongoClient
import requests
import json
import sys
import os

sys.path.insert(0, os.getcwd())
import consts

app = Flask(__name__)
le = None
PORT = None


def add_or_update_qa_worker(qa, worker):
    uri = f"mongodb://{consts.MONGO_DB_MAIN_SERVER['primary']}"
    client = MongoClient(uri)
    db = client[consts.DB_NAME]
    qa_collection = db[consts.QA_COLLECTION]

    result = qa_collection.find_one({"Question": qa["Question"]}, {"_id": 0})
    if result is not None:
        ans = qa['Answers'][0]['Answer']
        answer_exists = False
        for answer in result['Answers']:
            if ans == answer['Answer']:
                answer_exists = True
                break
        if not answer_exists:
            # update.
            update_result = qa_collection.update_one({"Question": qa["Question"]},
                                                     {'$push': {'Answers': qa['Answers'][0]}})
            if update_result.raw_result['nModified'] >= 1:
                msg = "Done"
                return make_response(jsonify(msg), 200)
        else:
            msg = "This answer is already exists."
            return make_response(jsonify(msg), 200)
    else:
        # insert new one.
        insert_result = qa_collection.insert_one(qa)

        if insert_result.inserted_id is not None:
            msg = "Done"
            return make_response(jsonify(msg), 200)

    msg = "Error"
    return make_response(jsonify(msg), 500)


def get_leader(zk, nodes_path):
    children = zk.get_children(nodes_path)
    for child in children:
        address, job, status = zk.get(f"{nodes_path}/{child}")[0].decode().split(",")
        if job == consts.LEADER:
            return child, address, status
    return None


def verify_req_sender_is_leader(zk, nodes_path, req):
    try:
        leader = get_leader(zk, nodes_path)
        leader_domain = leader[1]
        sender_domain = req.headers.get('Sender-Domain')
        if leader_domain == sender_domain:
            return True
    except:
        return False

    return False


@app.route("/get_qa_query", methods=['POST'])
def get_qa_query():
    body = json.loads(request.json)
    term = body["term"]
    worker = body["worker"]
    shard_address = body["shard_address"]
    shard_primary_address = shard_address["primary"]

    # verify if the request sender is the leader.
    if not verify_req_sender_is_leader(le.zk, consts.BASE_PATH, request):
        msg = "You're not the leader (Unauthorized request)."
        return make_response(jsonify(msg), 401)

    uri = f"mongodb://{shard_primary_address}"
    client = MongoClient(uri)
    db = client[consts.DB_NAME]
    qa_collection = db[consts.QA_COLLECTION]
    qa = list(qa_collection.find({}, {"_id": 0}))

    # TODO: run TF-IDF
    # TODO: qa object need to contain the tf-idf score.

    return qa


@app.route("/add_qa", methods=['POST'])
def add_qa():
    body = json.loads(request.json)
    qa = body["qa"]
    worker = body["worker"]
    return add_or_update_qa_worker(qa, worker)


def run(l_e, port):
    global le, PORT
    print("worker: run...")
    le = l_e
    PORT = port
    app.run(port=PORT, debug=True, use_reloader=False)
