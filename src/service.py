import flask
from flask import request
import base64
import json
import hashlib
import datetime
import re
import db_operation
import s3_operation


app = flask.Flask(__name__)
db_executor = db_operation.DBExecutor()
s3_executor = s3_operation.S3Executor()


@app.route('/v1/user/self', methods=['GET'])
def get_user_info():
    auth = get_authentication(request.headers)
    if auth == "":
        return "Unauthorized", 401

    user_name, password = auth.split(":")
    result = check_user_exist(user_name, password)
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
        result = check_user_exist(user_name, password)
        if result:
            sql = "update health set "
            for key in to_update:
                value = json_data[key]
                if key == "password":
                    value = hashlib.md5(value.encode('utf-8')).hexdigest()
                sql += "%s = \"%s\", " % (key, value)

            sql += "account_updated = \"%s\"" % (datetime.datetime.now())

            sql += " where user_name=\"%s\";" % user_name
            print(sql)
            db_executor.execute(sql)

            return "User updated", 204
        else:
            return "Bad request", 400
    except json.decoder.JSONDecodeError:
        return "Bad request", 400


@app.route('/v1/user/self/pic', methods=['POST'])
def update_user_profile_image():
    auth = get_authentication(request.headers)
    if auth == "":
        return "Unauthorized", 401

    user_name, password = auth.split(":")
    result = check_user_exist(user_name, password)
    if result:
        file = request.files["image"]
        img_data = file.read()

        image_filename = file.filename
        image_upload = str(datetime.date.today())
        image_id = hashlib.md5((user_name + image_upload).encode('utf-8')).hexdigest()
        image_url = s3_executor.bucket_name + "/" + image_id

        if not s3_executor.post(key=image_id, data=img_data):
            return "Bad request", 400

        sql = "update health set "
        sql += "image_filename = \"%s\", " % image_filename
        sql += "image_id = \"%s\", " % image_id
        sql += "image_url = \"%s\", " % image_url
        sql += "image_upload = \"%s\" " % image_upload
        sql += "where user_name = \"%s\";" % user_name
        print(sql)
        if db_executor.execute(sql):
            return "Profile pic added/updated", 201
        else:
            return "Bad request", 400
    else:
        return "Bad request", 400


@app.route('/v1/user/self/pic', methods=['GET'])
def get_user_profile_image():
    auth = get_authentication(request.headers)
    if auth == "":
        return "Unauthorized", 401

    user_name, password = auth.split(":")
    result = check_user_exist(user_name, password)
    if result:
        data = result[0]
        if data[7] is not None:
            resp_json = json.dumps({"image_filename": data[8],
                                    "image_id": data[7],
                                    "image_url": data[9],
                                    "image_upload": str(data[10]),
                                    "user_id": data[0]})
            resp = flask.jsonify(resp_json)
            resp.headers["Content-Type"] = "application / json"
            return resp, 200
        else:
            return "Not found", 404
    else:
        return "Bad request", 400


@app.route('/v1/user/self/pic', methods=['DELETE'])
def delete_user_profile_image():
    auth = get_authentication(request.headers)
    if auth == "":
        return "Unauthorized", 401

    user_name, password = auth.split(":")
    result = check_user_exist(user_name, password)
    if result:
        data = result[0]
        if data[7] is not None:
            sql = "update health set "
            sql += "image_filename = null, "
            sql += "image_id = null, "
            sql += "image_url = null, "
            sql += "image_upload = null "
            sql += "where user_name = \"%s\";" % user_name

            if s3_executor.delete(key=data[7]):
                return "No Content", 204
            else:
                return "Bad request", 400
        else:
            return "Not found", 404
    else:
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
        success = db_executor.execute(sql)
        if success:
            resp_json = json.dumps({"id": user_id,
                                    "first_name": first_name,
                                    "last_name": last_name,
                                    "user_name": username,
                                    "account_created": str(account_created),
                                    "account_updated": str(account_updated)})
            resp = flask.jsonify(resp_json)
            resp.headers["Content-Type"] = "application / json"
            return resp, 201
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


def check_user_exist(user_name, password):
    hash_psd = hashlib.md5(password.encode('utf-8')).hexdigest()
    sql = "select * from health where user_name=\"%s\" and password=\"%s\";" % (user_name, hash_psd)
    return db_executor.execute_and_get_result(sql)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3333, debug=False, processes=True)
