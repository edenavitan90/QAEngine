from pymongo import MongoClient
from pymongo.collection import Collection, ReturnDocument

URI = f"mongodb://localhost:27023"
client = MongoClient(URI)
db = client["QAEngine"]

qa_collection = db["test"]

# TODO: delete it
qa = {"Question": "what is java update scheduler?", "Answers": [{"Answer": "Java Update scheduler will check for "
                                                                           "newer Java updates and notify you at the "
                                                                           "scheduled frequency.", "Likes": 0,
                                                                 "Dislikes": 0}]}

result = qa_collection.insert_one(qa)
print("qa:", result)
print("type(qa):", type(result))
