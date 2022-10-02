from pymongo import MongoClient
from pymongo.collection import Collection, ReturnDocument
import consts

URI = f"mongodb://localhost:27012"
client = MongoClient(URI)
db = client["QAEngine"]
qa_collection = db["qa_data"]

obj = qa_collection.find({})
print(len(list(obj)))