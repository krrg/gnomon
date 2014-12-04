from app.views.api import api
from flask import request, session, jsonify, abort, make_response
from app.__init__ import db
from functools import wraps


@api.route('/auth', methods=['POST'])
def api_auth_login():
    print "SLKDJGLSKDJGLSKDJGLKSDJG"
    body = request.get_json(force=True)

    print body

    try:
        if attempt_auth_login(body['username'], body['password']):
            return jsonify({
                "success": True
            })
        else:
            return make_response(jsonify({
                "error": {
                    "msg": "Invalid username or password."
                }
            }), 401)
    except KeyError as e:
        print e
        return make_response(jsonify({
            "error": {
                "msg": "Malformed request--missing username or password field."
            }
        }), 400, None)


@api.route('/auth', methods=['DELETE'])
def api_auth_logout():
    session.clear()  # I have my dubious doubts about whether this is actually working.
    return jsonify({
        "success": True,
        "msg": "Logged out."
    })


# http://flask.pocoo.org/docs/0.10/patterns/viewdecorators/
def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'userid' not in session:
            return make_response(jsonify({
                "error": {
                    "msg": "You must be logged in to access this resource!"
                }
            }), 401)
        else:
            return f(*args, **kwargs)
    return decorated_function


def attempt_auth_login(username, password):
    from app.views.api.users import PasswordAuth
    user = db['users'].find_one({"username": username})
    if not user:
        return False

    stored_hash = user['password']
    salt = user['password_salt']
    attempted_hash = PasswordAuth.hash_pw(password, salt)

    if attempted_hash == stored_hash:
        session['userid'] = user['_id']
        return True
    else:
        return False
