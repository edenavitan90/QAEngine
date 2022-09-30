from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)


@app.route("/")
@app.route("/login")
def login():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)

