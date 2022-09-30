from flask import Flask
import sys
import os
import socket

# sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.getcwd())

print(sys.path)
from leader_election import LeaderElection

BASE_PATH = '/backend_znodes'
app = Flask(__name__)

@app.route("/", )
def hello_world():
    return f"<p>{le.server_stats}</p>"


if __name__ == '__main__':
    try:
        sock = socket.socket()
        sock.bind(('', 0))
        PORT = sock.getsockname()[1]

        le = LeaderElection(f"localhost:2181", f"localhost:{PORT},Worker", BASE_PATH)
        le.register()
        app.run(port=PORT, debug=True, use_reloader=False)
    finally:
        le.zk.stop()
        le.zk.close()
