BASE_PATH = '/backend_znodes'
ZNODE_PREFIX = '/a_'

LEADER = "Leader"
WORKER = "Worker"

FREE = "Free"
BUSY = "Busy"


# MongoDB config:
DB_NAME = "QAEngine"
QA_COLLECTION = "qa_data"
NUMBER_OF_SHARD = 2
SHARDS_ADDRESS = [{"name": "a", "primary": "localhost:27010", "secondary": "localhost:27011"},
                  {"name": "b", "primary": "localhost:27012", "secondary": "localhost:27013"}]
