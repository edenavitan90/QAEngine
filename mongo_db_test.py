from pymongo import MongoClient

URI = f"mongodb://localhost:27023"

client = MongoClient(URI)
my_db = client["QAEngine"]
print(my_db["users"])

"""mycol = client["QAEngine"]["users"]
for x in mycol.find():
  print(x)"""

# db.command('enableSharding',  'QAEngine_DB')
# db.command({'shardCollection': 'QAEngine_DB.QAEngine_DB_QA_Data', 'key': {'Question': 1}})
# db.command('listCommands')

