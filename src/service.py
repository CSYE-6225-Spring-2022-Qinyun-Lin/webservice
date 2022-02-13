import flask


app = flask.Flask(__name__)


# http://localhost:9999/
# return: 200
@app.route('/', methods=['GET', 'POST'])
aaaaadef call_service():
    # resp_json = json.dumps({"readOnly": False,
    #                         "writeOnly": False,
    #                         "multipleOf": 1,
    #                         "minimum": 0,
    #                         "maximum": 1})
    resp = flask.jsonify({"code": 200})
    resp.headers["Content-Type"] = "application / json"
    return resp, 200


if __name__ == '__main__':
    app.run(port=9999, debug=False, processes=True)
