import leader_routes
import worker_routes
import sys
import os
import socket

sys.path.insert(0, os.getcwd())
from leader_election import LeaderElection
import consts


if __name__ == '__main__':
    try:
        sock = socket.socket()
        sock.bind(('', 0))
        PORT = sock.getsockname()[1]

        le = LeaderElection(f"localhost:2181", f"localhost:{PORT},{consts.WORKER},{consts.FREE}", consts.BASE_PATH)
        le.register()

        if le.is_leader():
            leader_routes.run(le, PORT)
        else:
            worker_routes.run(le, PORT)
    finally:
        le.zk.stop()
        le.zk.close()
