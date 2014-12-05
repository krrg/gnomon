from app.views.api import api, expect_json_body
from flask import request, session, jsonify, abort, make_response
from app.__init__ import db
from auth import auth_required

# Mongo id lookups
from bson import ObjectId

@api.route("/jobs", methods=['GET'])
@auth_required
def api_jobs_list():

