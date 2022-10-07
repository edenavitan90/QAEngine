from pymongo.collection import Collection, ReturnDocument
from pymongo import MongoClient
import json
import sys
import os

sys.path.insert(0, os.getcwd())
import consts


def get_and_increment_next_qa_index(counter_collection: Collection):
    return counter_collection.find_one_and_update({'_id': "qa_id"},
                                                  {'$inc': {"counter": 1}},
                                                  return_document=ReturnDocument.AFTER)["counter"]


def insert_one_qa(counter_collection: Collection, qa_collection: Collection, qa_item):
    qa_item["qa_id"] = get_and_increment_next_qa_index(counter_collection)
    return qa_collection.insert_one(qa_item)


f = open('full_data.json')
full_data = json.load(f)

URI = f"mongodb://localhost:27023"
client = MongoClient(URI)

db = client[consts.DB_NAME]
counter_collection = db[consts.COUNTER_COLLECTION]
qa_collection = db[consts.QA_COLLECTION]

counter_collection.update_one({'_id': "qa_id"},
                              {'$set': {"counter": 0}})

for item in full_data:
    insert_one_qa(counter_collection, qa_collection, item)