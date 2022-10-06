from pymongo.collection import Collection, ReturnDocument
from pymongo import MongoClient
import json
import sys
import os

sys.path.insert(0, os.getcwd())
import consts


f = open('data2.json')
data = json.load(f)

qas_data = []
impossible = 0

for data in data["data"]:
    for paragraph in data["paragraphs"]:
        for qa in paragraph["qas"]:
            if not qa["is_impossible"]:
                temp_answers = []
                answers = []
                for answer in qa["answers"]:
                    temp_answers.append(answer["text"])

                temp_answers = list(set(temp_answers))
                for answer in temp_answers:
                    ans = {"Answer": answer, "Likes": 0, "Dislikes": 0}
                    answers.append(ans)

                qa_temp = {"Question": qa["question"], "Answers": answers}
                qas_data.append(qa_temp)
            else:
                impossible += 1
f.close()

print(len(qas_data))
print(impossible)

with open('db_data_copy2.json', 'w') as f:
    json.dump(qas_data, f)

'''
###################################
def get_and_increment_next_qa_index(counter_collection: Collection):
    return counter_collection.find_one_and_update({'_id': "qa_id"},
                                                  {'$inc': {"counter": 1}},
                                                  return_document=ReturnDocument.AFTER)["counter"]


def insert_one_qa(counter_collection: Collection, qa_collection: Collection, qa_item):
    qa_item["qa_id"] = get_and_increment_next_qa_index(counter_collection)
    qa_collection.insert_one(qa_item)


URI = f"mongodb://localhost:27023"
client = MongoClient(URI)
db = client[consts.DB_NAME]

counter_collection = db[consts.COUNTER_COLLECTION]
qa_collection = db[consts.QA_COLLECTION]

# counter_collection.update_one({'_id': "qa_id"},
#                               {'$set': {"counter": 0}})
for item in qas_data:
    item["qa_id"] = get_and_increment_next_qa_index(counter_collection)
    qa_collection.insert_one(item)

'''
