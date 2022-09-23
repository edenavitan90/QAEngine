from pymongo import MongoClient

user_name = "admin"
password = "admin"
URI = f"mongodb+srv://{user_name}:{password}@qaengine.3k5sr9a.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(URI)
#db = client.test
db = client.admin
print(db)
db.command('enableSharding',  'QAEngine_DB')
# db.command({'shardCollection': 'QAEngine_DB.QAEngine_DB_QA_Data', 'key': {'Question': 1}})
# db.command('listCommands')

