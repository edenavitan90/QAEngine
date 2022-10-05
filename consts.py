TEST_MODE = False

TIMEOUT_2_MIN = 60 * 2  # 2 minutes timeout.

BASE_PATH = '/backend_znodes'
ZNODE_PREFIX = '/a_'

LEADER = "Leader"
WORKER = "Worker"

FREE = "Free"
BUSY = "Busy"

# MongoDB config:
DB_NAME = "QAEngine"

QA_TEST_COLLECTION = "qa_test"
TEST_COUNTER_COLLECTION = "test_counter"
TEST_USERS_COLLECTION = "test_users"

if TEST_MODE:
    QA_COLLECTION = QA_TEST_COLLECTION
    USERS_COLLECTION = TEST_USERS_COLLECTION
    COUNTER_COLLECTION = TEST_COUNTER_COLLECTION
else:
    QA_COLLECTION = "qa_data"
    USERS_COLLECTION = "users"
    COUNTER_COLLECTION = "counter"


MONGO_DB_MAIN_SERVER = {"name": "config-srv", "primary": "localhost:27023", "secondary": None}

NUMBER_OF_SHARD = 2
SHARDS_ADDRESS = [{"name": "a", "primary": "localhost:27010", "secondary": "localhost:27011"},
                  {"name": "b", "primary": "localhost:27012", "secondary": "localhost:27013"}]

STATUS_OK = [200, 201]

