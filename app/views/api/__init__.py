
from flask import Blueprint, jsonify, session, request

api = Blueprint('api', __name__)


@api.route('/')
def api_default():
    return jsonify({
        "Response": "No method requested"
    })
