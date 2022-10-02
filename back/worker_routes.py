from flask import Flask, request
from pymongo import MongoClient
import json
import sys
import os

sys.path.insert(0, os.getcwd())
import consts

app = Flask(__name__)
le = None


@app.route("/get_qa_query", methods=['POST'])
def get_qa_query():
    body = json.loads(request.json)
    term = body["term"]
    worker = body["worker"]
    shard_address = body["shard_address"]
    shard_primary_address = shard_address["primary"]

    # TODO: verify if the request sender is the leader (check it with zk and the request port).

    uri = f"mongodb://{shard_primary_address}"
    client = MongoClient(uri)
    db = client[consts.DB_NAME]
    qa_collection = db[consts.QA_COLLECTION]
    qa = list(qa_collection.find({}, {"_id": 0}))

    # TODO: run TF-IDF

    return qa


def run(l_e, port):
    global le
    print("worker: run...")
    le = l_e
    app.run(port=port, debug=True, use_reloader=False)
