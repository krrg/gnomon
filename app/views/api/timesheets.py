from itertools import chain

from app.views.api import api
from apiwrappers import expect_json_body
from blist import sortedlist
from flask import request, session, jsonify, make_response
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
    from app.views.api.jobs import Job

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

        if Job.is_user_worker(hired_user_id, jobid):
            timesheet = db['timesheets'].find_one({"userid": hired_user_id, "jobid": jobid})
            return jsonify({
                "timesheet": {
                    "id": str(timesheet['_id']),
                    "msg": "Warning, the specified user {} already has an existing timesheet!".format(hired_user_id)
                }
            })

        tid = db['timesheets'].insert({
            "userid": hired_user_id,
            "jobid": jobid,
            "status": "active"  # TODO: Change this back to pending.
        })

        return jsonify({
            "timesheet": {
                "id": str(tid)
            }
        })

    except KeyError as e:
        return make_response(jsonify({
            "error": {
                "msg": "Your request was valid json, but it was missing the '{}' key.".format(str(e))
            }
        }), 400)


@api.route("/timesheets/<tid>", methods=['PUT'])
@auth_required
@expect_json_body
def api_timesheets_update(body, tid):
    timesheet = db['timesheets'].find_one({"_id": ObjectId(tid), "userid": session['userid']})
    if not timesheet:
        return make_response(jsonify({
            "error": {
                "msg": "Error, could not change status on timesheet.  Either you don't have permissions" +
                       "or the timesheet does not exist."
            }
        }), 400)

    if 'status' not in body or body['status'] != "active":
        return make_response(jsonify({
            "error": {
                "Could not find value on 'status' that is valid for this context."
            }
        }))

    timesheet['status'] = 'active'

    return jsonify({
        "timesheet": {
            "id": tid
        }
    })


@api.route("/timesheets/<tid>/clock", methods=['POST'])
@auth_required
@expect_json_body
def api_clock_append(body, tid):
    timesheet = db['timesheets'].find_one({"_id": ObjectId(tid), "userid": session['userid']})
    if not timesheet:
        return make_response(jsonify({
            "error": {
                "msg": "Error, could not change status on timesheet.  Either you don't have permissions" +
                       "or the timesheet does not exist."
            }
        }), 400)

    try:

        timein = body['clockIn']
        timeout = body['clockOut']

        clock = Clock(timesheet)
        if not clock.append(timein, timeout):
            return make_response(jsonify({
                "error": {
                    "msg": "Your times don't match up correctly!"
                }
            }), 400)
        else:
            timesheet['clockIn'] = clock.cin
            timesheet['clockOut'] = clock.cout

            db['timesheets'].save(timesheet)

            return jsonify({
                "id": tid,
                "msg": "Success"
            })
    except KeyError as e:
        return make_response(jsonify({
            "error": {
                "msg": "Missing key '{}'".format(str(e))
            }
        }), 400)


@api.route("/timesheets/<tid>/clock", methods=['PUT'])
@auth_required
@expect_json_body
def api_timesheet_update(body, tid):
    timesheet = db['timesheets'].find_one({"_id": ObjectId(tid), "userid": session['userid']})
    if not timesheet:
        return make_response(jsonify({
            "error": {
                "msg": "Error, could not change status on timesheet.  Either you don't have permissions" +
                       "or the timesheet does not exist."
            }
        }), 400)

    try:
        def save_timesheet():
            timesheet['clockIn'] = clock.cin
            timesheet['clockOut'] = clock.cout
            db['timesheets'].save(timesheet)

            return jsonify({
                "timesheet": {"id": tid}
            })

        if 'clockInOriginal' in body and 'clockInReplacement' in body:
            cin_orig = body['clockInOriginal']
            cin_repl = body['clockInReplacement']

            clock = Clock(timesheet)
            if not clock.replace_in(cin_orig, cin_repl):
                raise Clock.InvalidClockError("Invalid replacement times.")
            else:
                return save_timesheet()

        if 'clockOutOriginal' in body and 'clockOutReplacement' in body:
            cout_orig = body['clockOutOriginal']
            cout_repl = body['clockOutReplacement']

            clock = Clock(timesheet)
            if not clock.replace_out(cout_orig, cout_repl):
                raise Clock.InvalidClockError("Invalid replacement times.")
            else:
                return save_timesheet()

    except KeyError as e:
        return make_response(jsonify({
            "error": {
                "msg": "Missing key '{}'".format(str(e))
            }
        }), 400)
    except Clock.InvalidClockError as e:
        return make_response(jsonify({
            "error": {
                "msg": str(e)
            }
        }), 400)


@api.route("/timesheets/<tid>/clock/unix", methods=['DELETE'])
@auth_required
def api_clock_delete(tid):
    timesheet = db['timesheets'].find_one({"_id": ObjectId(tid), "userid": session['userid']})
    if not timesheet:
        return make_response(jsonify({
            "error": {
                "msg": "Error, could not change status on timesheet.  Either you don't have permissions" +
                       "or the timesheet does not exist."
            }
        }), 400)

    if 'clock' not in request.args:
        try:
            unixstamp = int(request.args)
            clock = Clock(timesheet)
            if clock.delete_stamp(unixstamp):
                timesheet['clockIn'] = clock.cin
                timesheet['clockOut'] = clock.cout
                db['timesheets'].save(timesheet)

                return jsonify({
                    "timesheet": {"id": tid}
                })
            else:
                return make_response(jsonify({
                    "error": {
                        "msg": "This timestamp is not present in the timesheet..."
                    }
                }), 400)
        except ValueError:
            return make_response(jsonify({
                "error": {
                    "msg": "The timestamp '{}' is not a valid timestamp.".format(unixstamp)
                }
            }), 400)


@api.route("/timesheets/<id>", methods=['DELETE'])
def api_timesheets_delete(id):
    make_response(jsonify({
        "error": {
            "msg": "Sorry, this hasn't been implemented yet."
        }
    }), 501)


class Clock:
    class InvalidClockError(Exception):
        pass

    def __init__(self, timesheet):
        self.cin = sortedlist(timesheet['clockIn'])
        self.cout = sortedlist(timesheet['clockOut'])

    def append(self, i, o):
        self.cin.append(i)
        self.cout.append(o)

        return self.__validate()

    def replace_in(self, in_orig, in_repl):
        self.cin.remove(in_orig)
        self.cin.add(in_repl)

        return self.__validate()

    def replace_out(self, out_orig, out_repl):
        self.cout.remove(out_orig)
        self.cout.add(out_repl)

        return self.__validate()

    def delete_stamp(self, stamp):
        if stamp in self.cout:
            index = self.cout.index(stamp)
        elif stamp in self.cin:
            index = self.cin.index(stamp)
        else:
            return False

        del self.cin[index]
        del self.cout[index]

    def __validate(self):
        if len(self.cin) != len(self.cout):
            return False

        for clock_out, clock_in in zip(self.cout, self.cin[1:]):
            if clock_in < clock_out:
                return False

        return True


class Timesheet:
    def __init__(self, timesheet):
        self.T = timesheet

    @staticmethod
    def get_user_viewable(jobId=None, organizationId=None, userId=None, status=None):
        mine = db['timesheets'].find({"userid": session['userid']})
        mine = map(Timesheet, mine) if mine else []
        owned = Timesheet.__get_owned_timesheets(orgid=organizationId)

        timesheet_map = {}

        # This part is pretty hacked---convert this to part of the mongo query or just use SQL in future renditions.
        for timesheet in chain.from_iterable([mine, owned]):
            t = timesheet.to_dict()
            if all([
                not jobId or t['jobId'] == jobId,  # Either they didn't specify a field or it must match.
                not userId or t['userId'] == userId,
                not status or t['status'] == status
            ]):
                timesheet_map[t['id']] = t

        return timesheet_map

    @staticmethod
    def __get_owned_timesheets(orgid=None):
        owned_jobs = []
        if not orgid:
            organizations = list(db['organizations'].find({"ownerid": session['userid']}))
        else:
            organizations = list(db['organizations'].find({"ownerid": session['userid'], "orgid": orgid}))

        if organizations:
            for org in organizations:
                jobs = db['jobs'].find({"orgid": str(org['_id'])}, {"jobid": 1})
                owned_jobs.extend(jobs if jobs else [])

        for job in owned_jobs:
            for t in db['timesheets'].find({"jobid": str(job['_id'])}):
                print t
                yield Timesheet(t)


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

    def to_dict(self):
        return {
            "id": str(self.T['_id']),
            "userId": self.T['userid'],
            "jobId": self.T['jobid'],
            "clockedIn": self.T['clockedIn'] if 'clockedIn' in self.T else [],
            "clockedOut": self.T['clockedOut'] if 'clockedOut' in self.T else [],
            "status": self.T['status']
        }

