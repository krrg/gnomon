# Flask
from app.views.api import api
from flask import request, session, jsonify, abort, make_response
from app.__init__ import db
from auth import auth_required


# Mongo id lookups
from bson import ObjectId

# Password hashing and salting
from os import urandom
import hashlib
import base64

# Time stamps
from datetime import datetime



@api.route('/users', methods=['GET'])
def api_users_list():
    users = []

    if 'jobId' in request.args:
        users.extend(api_users_filter_by_jobid(request.args['jobId']))
    elif 'username' in request.args:
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

@auth_required
def api_users_filter_by_jobid(jobid):

    from views.api.jobs import Job

    if not Job.is_user_owner(session['userid'], jobid):
        return make_response(jsonify({
            "error": {
                "msg": "You do not own the specified job."
            }
        }))

    users_in_job = db['timesheets'].find({"jobid": jobid}, {"userid": 1})

    return [x['userid'] for x in users_in_job]


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
    body = request.get_json(force=True)

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


def users_create(username, password, email, create_date=datetime.now()):
    salt = PasswordAuth.create_salt()
    pwhash = PasswordAuth.hash_pw(password, salt)

    modified_date = datetime.utcnow()

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

    def __init__(self):
        pass

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


@api.route('/users/<userid>', methods=['PUT'])
@auth_required
def api_users_update(userid):
    if str(userid) != str(session['userid']):
        return make_response(jsonify({
            "error": {
                "msg": "Error: You are not authorized to edit this user."
            }
        }), 401)
    try:
        body = request.get_json(force=True)
        user = db['users'].find_one({"_id": ObjectId(userid)})
        if any(map(lambda x: x in body, ['username', 'password', 'email'])):
            user['modified_date'] = datetime.utcnow()
        if 'username' in body:
            if db['users'].find_one(body['username']) is not None:
                return make_response(jsonify({
                    "error": {
                        "msg": "Specified username {} is already taken!".format(body['username'])
                    }
                }), 400, None)
            else:
                user['username'] = body['username']
        if 'password' in body:
            user['password_salt'] = PasswordAuth.create_salt()
            user['password'] = PasswordAuth.hash_pw(body['password'], user['password_salt'])
        if 'email' in body:
            user['email'] = body['email']

        db['users'].save(user)


        return make_response(jsonify({
            "msg": "success"
        }))

    except KeyError:
        return make_response(jsonify({
            "error": {
                "msg": "Malformed request.  No more information was available."
            }
        }), 400)
    except TypeError:
        return make_response(jsonify({
            "error": {
                "msg": "The specified user id {} could not be found!".format(userid)
            }
        }))




