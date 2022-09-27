import pandas as pd
import json
from pymongo import MongoClient
from pymongo.collection import Collection, ReturnDocument

data1 = pd.read_csv("S10_question_answer_pairs.txt", sep="\t").dropna()
data2 = pd.read_csv("S10_question_answer_pairs.txt", sep="\t").dropna()
data3 = pd.read_csv("S09_question_answer_pairs.txt", sep="\t").dropna()

concat_data = pd.concat([data1, data2, data3], axis=0)
data = concat_data.drop(columns=['ArticleTitle', 'DifficultyFromQuestioner', 'DifficultyFromAnswerer', 'ArticleFile'])

dict = data.groupby(['Question'], dropna=True).apply(lambda x: list(set(x['Answer'].tolist()))).to_dict()
print(dict)

item_list = []
for key, value in dict.items():
    temp_dict = {}
    temp_dict["Question"] = key
    temp_dict["Answers"] = value

    item_list.append(temp_dict)

with open('data.json', 'w') as f:
    json.dump(item_list, f)


###################################
def get_and_increment_next_qa_index(counter_collection: Collection):
    return counter_collection.find_one_and_update({'_id': "qa_id"},
                                                 {'$inc': {"counter": 1}},
                                                 return_document=ReturnDocument.AFTER)["counter"]

URI = f"mongodb://localhost:27023"
client = MongoClient(URI)
db = client["QAEngine"]

counter_collection = db["counter"]
qa_collection = db["qa_data"]

for item in item_list:
    item["qa_id"] = get_and_increment_next_qa_index(counter_collection)
    qa_collection.insert_one(item)





