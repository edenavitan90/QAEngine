from flask import Flask, request, render_template, redirect, url_for, session
from kazoo.client import KazooClient
import requests
import hashlib
import json
import sys
import os

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
            session["success_register"] = False
            return redirect(url_for("login"))
    else:
        if "user" in session:
            return redirect(url_for("platform"))
        is_success = session.pop("success_register", None)
        return render_template('login.html', success=is_success)


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

            if response.status_code in consts.STATUS_OK:
                session["user"] = usr
                return redirect(url_for("platform"))
            else:
                session["success_register"] = False
                return redirect(url_for("register"))
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
    query = ''
    if request.args:
        # A GET method with query.
        args = request.args
        likes = args.get('likes', '')
        dislikes = args.get('dislikes', '')

        query = args.get('query', '')
        if query == '':
            query = session.get('query', '')

        leader = get_leader(zk, consts.BASE_PATH)
        leader_domain = leader[1]

        if likes != '' or dislikes != '':
            if likes != '':
                type = "Likes"
                qa_id, answer = likes.split("-", maxsplit=1)
            else:
                type = "Dislikes"
                qa_id, answer = dislikes.split("-", maxsplit=1)

            body = {"qa_id": qa_id, "answer": answer, "type": type}

            url = f"http://{leader_domain}/update_question_rank"
            response = requests.post(url=url, json=json.dumps(body))
            # We cant just alert box with an error had occurred when like or so..
            if response.status_code not in consts.STATUS_OK:
                pass  # alert box saying error had occurred?

        if query != '':
            session["query"] = query
            url = f"http://{leader_domain}/get_qa_query?term={query}"
            response = requests.get(url=url)
            qas = response.json()
            for qa in qas:
                for answer in qa["Answers"]:
                    answer["Relevant"] = answer["Likes"] - answer["Dislikes"]
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

        if response.status_code in consts.STATUS_OK:
            session["success_register"] = True
            return redirect(url_for("new_question"))
        else:
            session["success_register"] = False
            return redirect(url_for("new_question"))

    if "user" in session:
        usr = session["user"]
        is_success = session.pop("success_register", None)
        return render_template('new_question.html', user=usr, success=is_success)
    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


if __name__ == '__main__':
    zk = KazooClient(hosts='localhost:2181')
    zk.start()
    app.run(debug=True, use_reloader=False)

