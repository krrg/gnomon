from app.views.api import api
from flask import jsonify



@api.route("/export")
def api_export_all():

    from views.api.organizations import api_organizations_list
    from views.api.timesheets import api_timesheet_list

    organizations = api_organizations_list()
    timesheets = api_timesheet_list()

    return jsonify({
        "organizations": str(organizations),
        "timesheets": str(timesheets)
    })
