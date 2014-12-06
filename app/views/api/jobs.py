from apiwrappers import expect_json_body
from app.views.api import api
from flask import request, session, jsonify, abort, make_response
from auth import auth_required
from app.__init__ import db

# Mongo id lookups
from bson import ObjectId


@api.route("/jobs", methods=['GET'])
@auth_required
def api_jobs_list():
    orgid = request.args['organizationId'] if 'organizationId' in request.args else None
    name = request.args['name'] if 'name' in request.args else None

    return jsonify({
        "jobs": [{
            "id": str(job['_id']),
            "name": job['name'],
            "organizationId": job['orgid'],
            "description": job['description'] if 'description' in job else ""
        }] for job in Job.get_jobs_with_permissions(orgid=orgid, name=name)
    })


@api.route("/jobs/<jobid>", methods=['GET'])
@auth_required
def api_jobs_get(jobid):
    userid = session['userid']

    job = db['jobs'].find_one({"_id": ObjectId(jobid)})

    if Job.is_user_worker(userid, jobid) or Job.is_user_owner(userid, jobid):
        return jsonify({
            "job": {
                "id": jobid,
                "name": job['name'],
                "organizationId": job['orgid'],
                "description": job['description'] if 'description' in job else "",
            }
        })
    else:
        return make_response(jsonify({
            "error": {
                "msg": "Not authorized to access this job."
            }
        }), 401)


@api.route("/jobs", methods=['POST'])
@auth_required
@expect_json_body
def api_jobs_create(body):
    try:
        name = body['job']['name']
        orgid = body['job']['organizationId']
        description = body['job']['description']

        # Check ownership of organization.
        if not db['organizations'].find_one({"_id": ObjectId(orgid), "ownerid": session['userid']}):
            return make_response(jsonify({
                "error": {
                    "msg": "You don't own that organization; you can't add jobs to it!"
                }
            }), 401)

        jid = db['jobs'].insert({
            "name": name,
            "orgid": orgid,
            "description": description
        })

        return jsonify({
            "job": {
                "id": str(jid)
            }
        })

    except KeyError as e:
        return make_response(jsonify({
            "error": {
                "msg": "Missing required field {}".format(str(e))
            }
        }), 400)


@api.route("/jobs/<jid>", methods=['PUT'])
@auth_required
@expect_json_body
def api_jobs_update(body, jid):
    userid = session['userid']
    if not Job.is_user_owner(userid, jid):
        return make_response(jsonify({
            "error": {
                "msg": "Error: You don't own this job, thus you can't edit it."
            }
        }))

    job = db['jobs'].find_one({"_id": ObjectId(jid)})
    if not job:
        return make_response(jsonify({
            "error": {
                "msg": "Error, the specified job '{}' does not exist!".format(jid)
            }
        }))

    job['name'] = body['name'] if 'name' in body else job['name']
    job['description'] = body['description'] if 'description' in body else job['description']

    db['jobs'].save(job)

    return jsonify({
        "job": {
            "id": jid
        }
    })


@api.route("/jobs/<jid>", methods=['DELETE'])
def api_jobs_delete():
    return make_response(jsonify({
        "error": {
            "msg": "Not yet implemented."
        }
    }))


class Job:

    def __init__(self):
        pass

    @staticmethod
    def is_user_owner(userid, jobid):
        from app.__init__ import db
        job = db['jobs'].find_one({"_id": ObjectId(jobid)})
        if job is None:
            return False

        orgid = job['orgid']
        org = db['organizations'].find_one({"_id": ObjectId(orgid)})
        if org is None:
            return False

        return org['ownerid'] == userid

    @staticmethod
    def is_user_worker(userid, jobid):
        return db['timesheets'].find_one({"userid": userid, "jobid": jobid}) is not None

    @staticmethod
    def get_jobs_user_in(userid):
        jobs_user_in = db['timesheets'].find({"userid": userid}, {"jobid": 1})
        return [(x['_id']) for x in jobs_user_in]

    @staticmethod
    def get_jobs_user_owns(userid):
        orgs_user_owned = db['organizations'].find({"ownerid": userid}, {"_id": 1})
        if not orgs_user_owned:
            return []

        orgs_ids = [str(x['_id']) for x in orgs_user_owned]

        jobs = db['jobs'].find({"orgid": {'$in': orgs_ids}}, {"_id": 1})

        return [(x['_id']) for x in jobs]

    @staticmethod
    def get_jobs_with_permissions(orgid=None, name=None):
        jobids = []
        jobids.extend(Job.get_jobs_user_in(session['userid']))
        jobids.extend(Job.get_jobs_user_owns(session['userid']))

        query = {"_id": {'$in': jobids}}
        if orgid:
            query['orgid'] = orgid
        if name:
            query['name'] = name

        job_permissioned_ids = [x for x in db['jobs'].find(query)]
        return job_permissioned_ids

    # The commented code below is now invalid.
    # @staticmethod
    # def is_user_worker(userid, jobid):
    #     job = db['jobs'].find_one({"_id": ObjectId(jobid)})
    #     if job is None:
    #         return False
    #
    #     return job['userid'] == userid

    # @staticmethod
    # def can_view_job(userid, jobid):
    #     return Job.is_user_worker(userid, jobid) or Job.is_user_owner(userid, jobid)
