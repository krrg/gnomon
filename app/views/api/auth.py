from app.views.api import api
from flask import request, session, jsonify, abort, make_response
from app.__init__ import db
from users import PasswordAuth


@api.route('/auth', methods=['POST'])
def api_auth_login():
    body = request.get_json(force=True)

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
            }))
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


def attempt_auth_login(username, password):
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
