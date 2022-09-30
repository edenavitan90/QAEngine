from flask import Flask, request

app = Flask(__name__)
le = None

@app.route("/get_qa_query/", methods=['GET'])
def get_qa_query():
    # TODO: change function
    term = request.args.get('term')
    return f"{term}, {le.znode_name}"


def run(l_e, port):
    global le
    print("worker: run...")
    le = l_e
    app.run(port=port, debug=True, use_reloader=False)