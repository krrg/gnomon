from functools import wraps
from flask import Blueprint, jsonify, session, request, make_response
from app.views.api import api
from werkzeug.exceptions import BadRequest


@api.route('/')
def api_default():
    return jsonify({
        "Response": "No method requested"
    })


# http://flask.pocoo.org/docs/0.10/patterns/viewdecorators/
def expect_json_body(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            kwargs['body'] = request.get_json(force=True)
            if kwargs['body']:
                return f(*args, **kwargs)
            else:
                return make_response(jsonify({
                    "error": {
                        "msg": "Could not parse JSON.  Is it well-formed?"
                    }
                }), 400)
        except BadRequest as e:
            return make_response(jsonify({
                "error": {
                    "msg": "Could not parse JSON.  Is it well-formed?",
                    "type": str(e)
                }
            }), 400)
    return decorated_function
