import os
from flask import Flask, request, render_template, redirect, url_for, session
import sys

# sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.getcwd())
import consts

app = Flask(__name__)
app.secret_key = "justforproject"


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


@app.route("/register")
def register():
    # TODO: recheck both passwords are equal on registration
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
    app.run(debug=True, use_reloader=False)

