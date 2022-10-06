from pymongo.collection import Collection, ReturnDocument
from pymongo import MongoClient
import random
import json
import sys
import os

sys.path.insert(0, os.getcwd())
import consts

"""
f = open('full_data_copy.json')
full_data = json.load(f)


data = {}
counter = 0
for d in full_data:
    if data.get(d["Question"]) is None:
        data[d["Question"]] = d
        counter += 1
    else:
        data[d["Question"]]["Answers"].extend(d["Answers"])

full_data = []
for d in data:
    full_data.append(data[d])


for item in full_data:
    for ans in item["Answers"]:
        ans["Dislikes"] = random.randint(0, 5)
        ans["Likes"] = random.randint(0, 9)

print(len(full_data))
with open('full_data.json', 'w') as f:
    json.dump(full_data, f)
"""

f = open('full_data.json')
full_data = json.load(f)


URI = f"mongodb://localhost:27023"
client = MongoClient(URI)
db = client[consts.DB_NAME]

counter_collection = db[consts.COUNTER_COLLECTION]
qa_collection = db[consts.QA_COLLECTION]

counter_collection.update_one({'_id': "qa_id"},
                              {'$set': {"counter": 0}})

counter = 1
for item in full_data:
    # item["qa_id"] = get_and_increment_next_qa_index(counter_collection)
    # qa_collection.insert_one(item)
    # OR
    # insert_one_qa(counter_collection, qa_collection, item)
    item["qa_id"] = counter
    counter += 1
    # qa_collection.insert_one(item)

qa_collection.insert_many(full_data)
# """