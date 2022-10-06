from pymongo.collection import Collection, ReturnDocument
from pymongo import MongoClient
import pandas as pd
import json
import consts

data1 = pd.read_csv("qa/S10_question_answer_pairs.txt", sep="\t").dropna()
data2 = pd.read_csv("qa/S10_question_answer_pairs.txt", sep="\t").dropna()
data3 = pd.read_csv("qa/S09_question_answer_pairs.txt", sep="\t").dropna()

concat_data = pd.concat([data1, data2, data3], axis=0)
data = concat_data.drop(columns=['ArticleTitle', 'DifficultyFromQuestioner', 'DifficultyFromAnswerer', 'ArticleFile'])

data_dict = data.groupby(['Question'], dropna=True).apply(lambda x: list(set(x['Answer'].tolist()))).to_dict()

item_list = []
for key, value in data_dict.items():
    temp_dict = {}
    temp_dict["Question"] = key

    answers = []
    for ans in value:
        answers.append({"Answer": ans, "Likes": 0, "Dislikes": 0})

    temp_dict["Answers"] = answers
    item_list.append(temp_dict)

with open('db_data_copy.json', 'w') as f:
    json.dump(item_list, f)


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

counter_collection.update_one({'_id': "qa_id"},
                              {'$set': {"counter": 0}})

counter = 1
for item in item_list:
    # item["qa_id"] = get_and_increment_next_qa_index(counter_collection)
    # qa_collection.insert_one(item)
    # OR
    # insert_one_qa(counter_collection, qa_collection, item)
    item["qa_id"] = counter
    counter += 1
    qa_collection.insert_one(item)





