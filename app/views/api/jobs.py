from apiwrappers import expect_json_body
from app.views.api import api
from flask import request, session, jsonify, abort, make_response
from auth import auth_required

# Mongo id lookups
from bson import ObjectId


@api.route("/jobs", methods=['GET'])
@auth_required
def api_jobs_list():
    abort(501)


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
