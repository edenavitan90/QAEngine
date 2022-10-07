# Important:
#     this script must run in mongodb root folder.
#
# Definitions:
#     num_of_config_replica = 3   -> ['config-srv-0', 'config-srv-1', 'config-srv-2']
#     num_of_shards = 2           -> ['a', 'b']
#     num_of_shards_replica = 2

mkdir config-srv-0 config-srv-1 config-srv-2
mkdir shard-a0 shard-a1 shard-b0 shard-b1

mongod --configsvr -replSet config-srv --dbpath config-srv-0 --port 27020 --fork --logpath log.cfg0
mongod --configsvr -replSet config-srv --dbpath config-srv-1 --port 27021 --fork --logpath log.cfg1
mongod --configsvr -replSet config-srv --dbpath config-srv-2 --port 27022 --fork --logpath log.cfg2

mongosh --port 27020
rs.initiate()
rs.add("localhost:27021")
rs.add("localhost:27022")
exit

mongod --shardsvr -replSet a --port 27010 --dbpath shard-a0 --fork --logpath log.a0
mongod --shardsvr -replSet a --port 27011 --dbpath shard-a1 --fork --logpath log.a1

mongod --shardsvr -replSet b --port 27012 --dbpath shard-b0 --fork --logpath log.b0
mongod --shardsvr -replSet b --port 27013 --dbpath shard-b1 --fork --logpath log.b1

mongosh --port 27010
rs.initiate()
rs.add("localhost:27011")
exit

mongosh --port 27012
rs.initiate()
rs.add("localhost:27013")
exit

mongos --configdb "config-srv/localhost:27020,localhost:27021,localhost:27022" --port 27023 --fork --logpath log.mongos1

mongosh --port 27023
sh.addShard("a/localhost:27010")
sh.addShard("b/localhost:27012")

use QAEngine
db.createCollection("counter")
db.counter.insertOne({"_id": "qa_id", "counter": 0})
db.createCollection("users")
db.createCollection("qa_data")
show collections
show dbs

# db.qa_data.createIndex({ _id: "hashed"}) # needed?
sh.shardCollection('QAEngine.qa_data', {'qa_id':'hashed'})
db.qa_data.getShardDistribution()

use config
db.shards.find()

