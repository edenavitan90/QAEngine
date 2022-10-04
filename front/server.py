from flask import Flask, request, render_template, redirect, url_for, session
from kazoo.protocol.states import EventType, WatchedEvent
from kazoo.client import KazooClient, KazooState
import os
import sys
import hashlib
import requests
import json

# sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.getcwd())
import consts

app = Flask(__name__)
app.secret_key = "justforproject"


def get_leader(zk, nodes_path):
    children = zk.get_children(nodes_path)
    for child in children:
        address, job, status = zk.get(f"{nodes_path}/{child}")[0].decode().split(",")
        if job == consts.LEADER:
            return child, address, status
    return None


@staticmethod
def connection_status_listener(state):
    if state == KazooState.LOST:
        print('session to zookeeper was lost')  # Register somewhere that the session was lost
    elif state == KazooState.SUSPENDED:
        print('disconnected from zookeeper')  # Handle being disconnected from Zookeeper
    else:
        print('connected to zookeeper')  # Handle being connected/reconnected to Zookeeper


@app.route("/", methods=["POST", "GET"])
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        usr = request.form["usrname"]
        password = request.form["pwd"]
        # TODO: Add checking credentials mechanism, obviously, will hash password on registration and checking.

        session["user"] = usr  # actually in cookies
        return redirect(url_for("platform"))
    else:
        if "user" in session:
            return redirect(url_for("platform"))
        return render_template('login.html')


@app.route("/register", methods=["POST", "GET"])
def register():
    # TODO: recheck both passwords are equal on registration
    if request.method == "POST":
        usr = request.form["usrname"]
        password = request.form["pwd"]
        repassword = request.form["repwd"]
        if password == repassword:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            body = {"username": usr, "password": hashed_password}

            leader = get_leader(zk, consts.BASE_PATH)
            leader_domain = leader[1]

            url = f"http://{leader_domain}/get_qa_query"
            response = requests.post(url=url, json=json.dumps(body))
            print(response.content)
            return redirect(url_for("login"))

    return render_template('register.html')


@app.route("/platform")
def platform():
    if "user" in session:
        usr = session["user"]
        return render_template('platform.html', user=usr)

    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


if __name__ == '__main__':
    zk = KazooClient(hosts='localhost:2181')
    zk.start()
    zk.add_listener(connection_status_listener)  # notify about connection change
    app.run(debug=True, use_reloader=False)

