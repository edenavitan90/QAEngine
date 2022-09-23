import pandas as pd
import json

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