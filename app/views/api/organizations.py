from app.views.api import api
from apiwrappers import expect_json_body
from flask import request, session, jsonify, abort, make_response
from app.__init__ import db
from auth import auth_required

# Mongo id lookups
from bson import ObjectId


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
@expect_json_body
def api_organization_create(body):
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
@expect_json_body
def api_organization_update(orgid, body):
    try:
        name = body['organization']['name']
        org = db['organizations'].find_one({"_id": ObjectId(orgid), "ownerid": session['userid']})
        if org is None:
            return make_response(jsonify({
                "error": {
                    "msg": "Organization with id '{}' could not be found (do you own this organization?)".format(orgid)
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


@api.route("/organization/<orgid>", methods=['DELETE'])
@auth_required
def api_organization_delete(orgid):
    return make_response(jsonify({
        "error": {
            "msg": "Not yet implemented."
        }
    }), 501)
    # org = db['organizations'].find_one({"_id": ObjectId(orgid), "ownerid": session['userid']})
    # if org is None:
    #     return make_response(jsonify({
    #         "error": {
    #             "msg": "Could not find organization '{}' (are you the owner?)".format(orgid)
    #         }
    #     }))
    # else:
    #     db['organizations'].remove({"_id": ObjectId(orgid)})
    #     return make_response(jsonify({
    #         "success": {
    #             "msg": "Group successfully removed.",
    #             "id": orgid
    #         }
    #     }))
