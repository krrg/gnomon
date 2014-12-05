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


@api.route("/timesheet")
def api_timesheet_list():
    abort(501)

