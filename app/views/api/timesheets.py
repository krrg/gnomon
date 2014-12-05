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
        }))


@api.route("/timesheets", methods=['GET'])
@auth_required
def api_timesheet_list():
    abort(501)


class Timesheet:

    def __init__(self, timesheet):
        self.T = timesheet

    @staticmethod
    def get_user_viewable():
        mine = db['timesheets'].find({"userid": session['userid']})
        mine = mine if mine else []

        owned = Timesheet.__get_owned_timesheets()

        # Need to index by ObjectID

    @staticmethod
    def __get_owned_timesheets():
        owned = []
        organizations = db['organizations'].find({"ownerid": session['userid']})
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
                "userId": self.T.userid,
                "jobId": self.T.jobid,
                "clockedIn": self.T.clockedIn if self.T.clockedIn else [],
                "clockedOut": self.T.clockedOut if self.T.clockedOut else [],
                "status": self.T.status
            }
        })
