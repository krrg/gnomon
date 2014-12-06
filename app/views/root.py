
from app import app
from flask import render_template, session, redirect
from app.views.wrappers import login_page_first


navlinks = [
    {
        "href": "/clockin",
        "text": "Clock"
    },
    {
        "href": "/timesheet",
        "text": "Timesheet"
    },
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

@app.route('/timesheet')
@app.route('/timesheet.html')
@login_page_first
def timesheet():
    return render_template("root/timesheet.html", navlinks=navlinks)

@app.route('/timesheet2')
@login_page_first
def timesheet2():
    return render_template("root/timesheet2.html")

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
