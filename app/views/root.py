
from app import app
from app.__init__ import db
from bson import ObjectId
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
    }
]


@app.route('/')
@app.route('/index.html')
def root_index():
    return render_template("root/index.html", homepage=True)

@app.route('/timesheet/<tid>')
@login_page_first
def timesheet(tid):
    # We need to check to make sure that they have permissions to view this.
    if not db['timesheets'].find_one({"_id": ObjectId(tid), "userid": session['userid']}):
        return "<html><body><h1>Error:</h1><h3>You don't have permission to view this timesheet!</h3></body></html>"

    return render_template("root/timesheet.html", navlinks=navlinks)

@app.route('/clockin')
@login_page_first
def clockin():
    return render_template("root/clockin.html", navlinks=navlinks)

@app.route('/manageOrganizations')
@login_page_first
def manageOrganizations():
    return render_template("root/manageOrganizations.html", navlinks=navlinks)

@app.route('/login')
def login():
    if 'userid' not in session:
        return render_template("root/login.html", loginpage=True)
    else:
        return redirect('/clockin')

@app.route('/searchUsers')
# @login_page_first
def searchUsers():
    return render_template("root/searchUsers.html", navlinks=navlinks)

@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')
