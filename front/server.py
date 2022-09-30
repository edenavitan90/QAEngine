from flask import Flask, request, render_template
import sys

# sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.getcwd())
import consts

app = Flask(__name__)


@app.route("/")
@app.route("/login")
def login():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)

