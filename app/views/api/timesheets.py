from itertools import chain
from app.views.api import api
from apiwrappers import expect_json_body
from flask import request, session, jsonify, abort, make_response
from app.__init__ import db
from auth import auth_required

# Mongo id lookups
from bson import ObjectId

# Job helper class
#


@api.route("/timesheets/<sheetid>", methods=['GET'])
@auth_required
def api_timesheet_get(sheetid):
    t = db['timesheets'].find_one({"_id": ObjectId(sheetid)})
    if not t:
        return make_response(jsonify({
            "error": {
                "msg": "Could not find timesheet '{}'".format(sheetid)
            }
        }), 404)

    timesheet = Timesheet(t)

    if timesheet.can_user_view(session['userid']):
        return timesheet.to_json()
    else:
        return make_response(jsonify({
            "error": {
                "msg": "You do not have permission to view this timesheet."
            }
        }), 401)


@api.route("/timesheets", methods=['GET'])
@auth_required
def api_timesheet_list():
    timesheet_map = Timesheet.get_user_viewable(*request.args)

    return jsonify(dict(timesheets=[
        x for x in timesheet_map.itervalues()
    ]))


@api.route("/timesheets", methods=['POST'])
@expect_json_body
@auth_required
def api_timesheet_create(body):

    from views.api.jobs import Job

    try:
        hired_user_id = body['timesheet']['userId']
        jobid = body['timesheet']['jobId']

        # Ensure that this user actually owns this job.
        if not Job.is_user_owner(session['userid'], jobid):
            return make_response(jsonify({
                "error": {
                    "msg": "You don't have permissions to create a timesheet for this job!"
                }
            }), 401)

        db['timesheet'].insert({
            "userid": hired_user_id,
            "jobid": jobid
        })

    except KeyError:
        return make_response(jsonify({
            "error": {
                "msg": "Your request was valid json, but it was missing required parameters."
            }
        }), 400)


@api.route("/timesheets/<id>", methods=['PUT'])
def api_timesheets_update(id):
    make_response(jsonify({
        "error": {
            "msg": "Sorry, this hasn't been implemented yet."
        }
    }), 501)


@api.route("/timesheets/<id>", methods=['DELETE'])
def api_timesheets_delete(id):
    make_response(jsonify({
        "error": {
            "msg": "Sorry, this hasn't been implemented yet."
        }
    }), 501)


class Timesheet:

    def __init__(self, timesheet):
        self.T = timesheet

    @staticmethod
    def get_user_viewable(jobId=None, organizationId=None, userId=None, status=None):
        mine = db['timesheets'].find({"userid": session['userid']})
        mine = mine if mine else []
        owned = Timesheet.__get_owned_timesheets(orgid=organizationId)

        timesheet_map = {}

        # This part is pretty hacked---convert this to part of the mongo query or just use SQL in future renditions.
        for timesheet in chain.from_iterable([mine, owned]):
            t = timesheet.to_json()
            if all([
                not jobId or t['jobId'] == jobId,       # Either they didn't specify a field or it must match.
                not userId or t['userId'] == userId,
                not status or t['status'] == status
            ]):
                timesheet_map[t['id']] = t

        return timesheet_map

    @staticmethod
    def __get_owned_timesheets(orgid=None):
        owned = []
        if not orgid:
            organizations = db['organizations'].find({"ownerid": session['userid']})
        else:
            organizations = db['organizations'].find({"ownerid": session['userid'], "orgid": orgid})

        if organizations:
            for org in organizations:
                jobs = db['jobs'].find({"orgid": org['_id']})
                owned.extend(jobs if jobs else [])
        return owned

    def can_user_view(self, userid):
        if self.T.userid == userid:
            return True  # The user is the worker

        owned_organizations = set([str(org['_id']) for org in db['organizations'].find({"ownerid": userid})])
        if len(owned_organizations) == 0:
            return False  # Then the user does not own any organizations.

        # Get the jobid from the timesheet
        jobid = self.T['jobid']
        job = db['jobs'].find_one({"_id": ObjectId(jobid)})

        if not job:
            return False  # Then the timesheet is (incidentally) invalid.

        orgid = job['orgid']

        return orgid in owned_organizations

    def to_json(self):
        return jsonify({
            "timesheet": {
                "id": str(self.T['_id']),
                "userId": self.T.userid,
                "jobId": self.T.jobid,
                "clockedIn": self.T.clockedIn if self.T.clockedIn else [],
                "clockedOut": self.T.clockedOut if self.T.clockedOut else [],
                "status": self.T.status
            }
        })
