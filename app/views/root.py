
from app import app
from flask import render_template
from views.wrappers import login_page_first


@app.route('/')
@app.route('/index.html')
def root_index():
    return render_template("root/index.html")

@app.route('/timesheet')
@app.route('/timesheet.html')
@login_page_first
def timesheet():
    return render_template("root/timesheet.html")

@app.route('/clockin')
@login_page_first
def clockin():
    return render_template("root/clockin.html")

@app.route('/manageOrganizations')
@login_page_first
def manageOrganizations():
    return render_template("root/manageOrganizations.html")

@app.route('/login')
def login():
    return render_template("root/login.html")

@app.route('/searchUsers')
# @login_page_first
def searchUsers():
    return render_template("root/searchUsers.html")
