from app.views.api import api
from flask import request, session, jsonify, abort, make_response
from app.__init__ import db

# Mongo id lookups
from bson import ObjectId

# Password hashing and salting
from os import urandom
import hashlib
import base64

# Time stamps
from datetime import datetime


# import flask


# @api.route('/users/<userid>', methods=['GET'])
# def api_users_list(userid):
#     return flask.make_response(flask.jsonify({
#         "Not yet implemented."
#     }), 501, None)

@api.route('/users', methods=['GET'])
def api_users_list():
    users = []
    if 'username' in request.args:
        filter = request.args['username']
        users.extend(db['users'].find({"username": filter}))
    else:
        users.extend(db['users'].find({}))

    return jsonify({
        "users": list(map(lambda user: {
            "id": str(user["_id"]),
            "username": user["username"]
        }, users))
    })


@api.route('/users/<userid>', methods=['GET'])
def api_users_get(userid):
    user = db['users'].find_one({"_id": ObjectId(userid)})
    if user:
        return make_response(jsonify({
            "user": {
                "id": str(user['_id']),
                "username": user['username'],
                "email": None
            }
        }), 200, None)
    else:
        return make_response(jsonify({
            "error": {
                "msg": "User '{}' does not exist!".format(userid)
            }
        }), 404, None)


@api.route("/users", methods=['POST'])
def api_users_create():
    print request.content_type
    body = request.get_json(force=True)
    print str(body)

    if body is None:
        return make_response(jsonify({
            'error': {
                'msg': 'Expected content type of application/json, but got \'' + request.content_type + '\' instead',
            }
        }), 400, None)

    try:
        username = body['user']['username']

        if db['users'].find_one({"username": username}) is not None:
            return make_response(jsonify({
                'error': {
                    'msg': 'Specified username already exists!',
                }
            }))

        password = body['user']['password']
        email = body['user']['email']
        _id = users_create(username, password, email)

        return make_response(jsonify({
            'user': {
                'id': str(_id)
            }
        }), 200, None)

    except KeyError:
        return make_response(jsonify({
            'error': {
                'msg': 'Malformed request: Missing key for username, password, or email!',
            }
        }), 400, None)


def users_create(username, password, email):
    salt = PasswordAuth.create_salt()
    pwhash = PasswordAuth.hash_pw(password, salt)

    create_date = datetime.now()
    modified_date = datetime.now()

    _id = db['users'].insert({
        "username": username,
        "email": email,
        "password": pwhash,
        "password_salt": salt,
        "create_date": create_date,
        "modified_date": modified_date
    })
    return _id


class PasswordAuth:

    @staticmethod
    def create_salt():
        SALT_LEN = 64
        return base64.b64encode(urandom(64))

    @staticmethod
    def hash_pw(password, salt):
        m = hashlib.sha512()
        m.update(salt)
        m.update(password)
        return base64.b64encode(m.digest())


