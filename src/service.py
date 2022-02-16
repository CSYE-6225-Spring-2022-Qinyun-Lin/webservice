import flask
from flask import request
import base64
import json
import hashlib
import datetime
import re
import db_operation


app = flask.Flask(__name__)


@app.route('/v1/user/self', methods=['GET'])
def get_user_info():
    auth = get_authentication(request.headers)
    if auth == "":
        return "Unauthorized", 401
    user_name, password = auth.split(":")
    hash_psd = hashlib.md5(password.encode('utf-8')).hexdigest()
    sql = "select * from health where user_name=\"%s\" and password=\"%s\";" % (user_name, hash_psd)
    result = db_operation.execute_and_get_result(sql)
    if result:
        data = result[0]
        resp_json = json.dumps({"id": data[0],
                                "first_name": data[3],
                                "last_name": data[4],
                                "user_name": data[1],
                                "account_created": str(data[5]),
                                "account_updated": str(data[6])})
        resp = flask.jsonify(resp_json)
        resp.headers["Content-Type"] = "application / json"
        return resp, 200
    else:
        return "Bad request", 400


@app.route('/v1/user/self', methods=['PUT'])
def update_user_info():
    auth = get_authentication(request.headers)
    if auth == "":
        return "Unauthorized", 401

    try:
        json_data = json.loads(request.data)
        to_update = json_data.keys()
        if len(to_update) == 0:
            return "Bad request", 400

        if "id" in to_update or "account_created" in to_update or "account_updated" in to_update:
            return "Bad request", 400

        user_name, password = auth.split(":")
        hash_psd = hashlib.md5(password.encode('utf-8')).hexdigest()
        sql = "select * from health where user_name=\"%s\" and password=\"%s\";" % (user_name, hash_psd)
        result = db_operation.execute_and_get_result(sql)
        if result:
            sql = "update health set "
            for key in to_update:
                value = json_data[key]
                if key == "password":
                    value = hashlib.md5(value.encode('utf-8')).hexdigest()
                sql += "%s = \"%s\", " % (key, value)

            sql += "account_updated = \"%s\"" % (datetime.datetime.now())

            sql += " where user_name=\"%s\" and password=\"%s\";" % (user_name, hash_psd)
            print(sql)
            db_operation.execute(sql)

            return "User updated", 204
        else:
            return "Bad request", 400
    except json.decoder.JSONDecodeError:
        return "Bad request", 400


@app.route('/healthz', methods=['GET'])
def health():
    return "OK", 200


@app.route('/v1/user', methods=['POST'])
def create_user():
    try:
        json_data = json.loads(request.data)
        first_name = json_data["first_name"]
        last_name = json_data["last_name"]
        password = json_data["password"]
        username = json_data["email_address"]
        account_created = str(datetime.datetime.now())
        account_updated = account_created

        reg_pattern = re.compile("^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$")
        if reg_pattern.match(username) is None:
            return "Bad request", 400

        user_id = hashlib.md5(account_created.encode('utf-8')).hexdigest()
        hash_psd = hashlib.md5(password.encode('utf-8')).hexdigest()

        sql = "INSERT INTO health " \
              "(id, user_name, password, first_name, last_name, account_created, account_updated) " \
              "VALUES (\"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\");" % \
              (user_id, username, hash_psd, first_name, last_name, account_created, account_updated)
        print(sql)
        success = db_operation.execute(sql)
        if success:
            return "User created", 201
        else:
            return "Bad request", 400

    except KeyError or json.decoder.JSONDecodeError:
        # return "Missing required field: %s" % e, 400
        return "Bad request", 400


def get_authentication(req_header):
    if req_header.get('Authorization') is None:
        print('Missing authentication!')
        return ""

    try:
        base64_auth = req_header['Authorization'].split(" ")[1]
        auth = base64.b64decode(base64_auth).decode('utf-8')
        # print(auth)
        return auth

    except Exception as e:
        print('Analysis authentication error: %s' % e)
        return ""


if __name__ == '__main__':
    app.run(port=3333, debug=False, processes=True)
