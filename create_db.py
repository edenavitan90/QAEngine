from pymongo.collection import Collection, ReturnDocument
from pymongo import MongoClient
import os


'''
Important:
    this script must run in mongodb root folder.
    
Definitions:
    num_of_config_replica = 3   -> ['config-srv-0', 'config-srv-1', 'config-srv-2']
    num_of_shards = 2           -> ['a', 'b']
    num_of_shards_replica = 2   -> []
'''


'''
mongod --configsvr -replSet config-srv --dbpath config-srv-0 --port 27020 --fork --logpath log.cfg0
'''

'''
config_srv_paths = ['config-srv-0', 'config-srv-1', 'config-srv-2']
for path in config_srv_paths:
    os.mkdir(path)
'''

client = MongoClient()
db = client.admin
print(db.command('listCommands'))




