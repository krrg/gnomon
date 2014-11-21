
from app import app
from flask import render_template


@app.route('/')
@app.route('/index.html')
def root_index():
    return render_template("root/index.html")

@app.route('/timesheet')
@app.route('/timesheet.html')
def timesheet():
    return render_template("root/timesheet.html")