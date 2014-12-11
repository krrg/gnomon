
from app import app
from flask import render_template, session, redirect
from app.views.wrappers import login_page_first


navlinks = [
    {
        "href": "/clockin",
        "text": "Clock"
    },
    # {
    #     "href": "/timesheet",
    #     "text": "Timesheet"
    # },
    {
        "href": "/manageOrganizations",
        "text": "Organizations"
    },
    {
        "href": "/searchUsers",
        "text": "Search Users"
    },
    {
        "href": "/export",
        "text": "Export"
    }
]




@app.route('/')
@app.route('/index.html')
def root_index():
    import app.views.api.users as users

    return render_template("root/index.html", homepage=True, navlinks=navlinks, username=users.get_current_username())

@app.route('/timesheet/<tid>')
@login_page_first
def timesheet(tid):
    import app.views.api.users as users
    # We need to check to make sure that they have permissions to view this.
    from app.views.api.timesheets import Timesheet
    if not Timesheet.by_id(tid).can_user_view(session['userid']):
        return "<html><body><h1>Error:</h1><h3>You don't have permission to view this timesheet!</h3></body></html>"

    return render_template("root/timesheet.html", navlinks=navlinks, username=users.get_current_username(), tid=tid)

@app.route('/clockin')
@login_page_first
def clockin():
    import app.views.api.users as users

    return render_template("root/clockin.html", navlinks=navlinks, username=users.get_current_username())

@app.route('/manageOrganizations')
@login_page_first
def manageOrganizations():
    import app.views.api.users as users

    return render_template("root/manageOrganizations.html", navlinks=navlinks, username=users.get_current_username())

@app.route('/login')
def login():

    if 'userid' not in session:
        return render_template("root/login.html", loginpage=True)
    else:
        return redirect('/clockin')

@app.route('/searchUsers')
# @login_page_first
def searchUsers():
    import app.views.api.users as users

    return render_template("root/searchUsers.html", navlinks=navlinks, username=users.get_current_username())

@app.route("/export")
@login_page_first
def export():
    import app.views.api.users as users
    return render_template("root/export.html", navlinks=navlinks, username=users.get_current_username())

@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')
