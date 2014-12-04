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


@api.route("/organizations", methods=['GET'])
@auth_required
def api_organizations_list():
    userid = session['userid']
    my_orgs = db['organizations'].find({"ownerid": ObjectId(userid)})

    if my_orgs:
        return jsonify({
            "organizations": [
                {
                    "id": str(org['_id']),
                    "name": org['name']
                } for org in my_orgs
            ]
        })
    else:
        return jsonify({
            "organizations": []
        })


@api.route("/organizations/<orgid>", methods=['GET'])
def api_organization_get(orgid):
    org = db['organizations'].find_one({"_id": ObjectId(orgid)})
    if org:
        return jsonify({
            "organization": {
                "id": orgid,
                "name": org['name'] if 'name' in org else None
            }
        })
    else:
        return make_response(jsonify({
            "error": {
                "msg": "Organization with id '{}' does not exist.".format(orgid)
            }
        }), 404)


@api.route("/organizations", methods=['POST'])
@auth_required
def api_organization_create():
    body = request.get_json(force=True)
    if body is None:
        return make_response(jsonify({
            "error": {
                "msg": "Could not parse JSON request!  Is it well-formed?"
            }
        }), 400)
    try:
        name = body['organization']['name']
        oid = db['organizations'].insert({
            'ownerid': session['userid'],
            'name': name
        })
        return jsonify({
            "organization": {
                "id": str(oid)
            }
        })
    except KeyError:
        return make_response(jsonify({
            "error": {
                "msg": "Missing required 'name' field."
            }
        }), 400)


@api.route("/organizations/<orgid>", methods=['PUT'])
@auth_required
def api_organization_update(orgid):
    body = request.get_json(force=True)
    if body is None:
        return make_response(jsonify({
            "error": {
                "msg": "Could not parse JSON request."
            }
        }))
    try:
        name = body['organization']['name']
        org = db['organizations'].find_one({"_id": ObjectId(orgid)})
        if org is None:
            return make_response(jsonify({
                "error": {
                    "msg": "Organization with id '{}' could not be found.".format(orgid)
                }
            }))
        org['name'] = name
        db['organizations'].save(org)

        return jsonify({
            "organization": {
                "id": orgid
            }
        })
    except KeyError:
        return make_response(jsonify({
            "error": {
                "msg": "Missing required field 'name'"
            }
        }))




