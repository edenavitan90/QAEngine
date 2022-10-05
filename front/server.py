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


# TODO: Move to a util file.
def get_leader(zk, nodes_path):
    children = zk.get_children(nodes_path)
    for child in children:
        address, job, status = zk.get(f"{nodes_path}/{child}")[0].decode().split(",")
        if job == consts.LEADER:
            return child, address, status
    return None


@app.route("/", methods=["POST", "GET"])
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        usr = request.form["usrname"]
        password = request.form["pwd"]
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        body = {"username": usr, "password": hashed_password}

        leader = get_leader(zk, consts.BASE_PATH)
        leader_domain = leader[1]

        url = f"http://{leader_domain}/login"
        response = requests.post(url=url, json=json.dumps(body))
        if response.status_code in consts.STATUS_OK:
            session["user"] = usr
            return redirect(url_for("platform"))
        else:
            # TODO: alert upon fail
            print(response.status_code)
            print(response.json())
            return redirect(url_for("login"))
    else:
        if "user" in session:
            return redirect(url_for("platform"))
        return render_template('login.html')


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        usr = request.form["usrname"]
        password = request.form["pwd"]
        repassword = request.form["repwd"]
        if password == repassword:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            body = {"username": usr, "password": hashed_password}

            leader = get_leader(zk, consts.BASE_PATH)
            leader_domain = leader[1]

            url = f"http://{leader_domain}/register"
            response = requests.post(url=url, json=json.dumps(body))

            # TODO: alert upon successful
            print(response.status_code)
            print(response.json())
            return redirect(url_for("login"))
        else:
            # Passwords are not matched
            session["success_register"] = False
            return redirect(url_for("register"))

    if "success_register" in session:
        is_success = session.pop("success_register", None)
        return render_template('register.html', success=is_success)
    return render_template('register.html')


@app.route("/platform", methods=["POST", "GET"])
def platform():
    qas = []
    qas_empty = False
    query = ""
    if request.args:
        # A GET method with query.
        args = request.args
        query = args.get('query', '')
        if query != '':
            # TODO: Take care of increment likes & dislikes
            # Upon increment -> just update in mongo and then GET method for the new data.

            leader = get_leader(zk, consts.BASE_PATH)
            leader_domain = leader[1]

            url = f"http://{leader_domain}/get_qa_query?term={query}"
            response = requests.get(url=url)
            qas = response.json()

            for qa in qas:
                for answer in qa["Answers"]:
                    if answer["Likes"] + answer["Dislikes"] == 0:
                        answer["Relevant"] = 0
                    else:
                        answer["Relevant"] = answer["Likes"] / (answer["Likes"] + answer["Dislikes"])
                qa["Answers"].sort(reverse=True, key=lambda y: y["Relevant"])

            if not qas:
                # No matched Questions/Answers in the DB
                qas_empty = True

    if "user" in session:
        usr = session["user"]
        return render_template('platform.html', user=usr, qas=qas, query=query, qas_empty=qas_empty)

    return redirect(url_for("login"))


@app.route("/new_question", methods=["POST", "GET"])
def new_question():
    if request.method == "POST":
        # Creating new question
        question = request.form["question"]
        answer = request.form["answer"]

        leader = get_leader(zk, consts.BASE_PATH)
        leader_domain = leader[1]

        body = {"question": question, "answer": answer}
        url = f"http://{leader_domain}/add_qa"

        response = requests.post(url=url, json=json.dumps(body))
        # TODO: alert response
        print(response.status_code)
        print(response.content.decode())

    if "user" in session:
        usr = session["user"]
        return render_template('new_question.html', user=usr)
    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


if __name__ == '__main__':
    zk = KazooClient(hosts='localhost:2181')
    zk.start()
    app.run(debug=True, use_reloader=False)

