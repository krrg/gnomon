from flask import Flask
from flask.ext import assets
import os

app = Flask(__name__)

#####################################################################
#  Flask assets
#####################################################################
env = assets.Environment(app)

# Tell flask-assets where to look for the Sassy CSS files.

env.load_path = [
    os.path.join(os.path.dirname(__file__), 'assets/scss')
]

env.register(
    'css_base',
    assets.Bundle(
        'base.scss',
        filters='scss',
        output='_gen/css_base.css'
    )
)

env.register(
    'css_timesheet',
    assets.Bundle(
        'timesheet.scss',
        filters='scss',
        output='_gen/css_timesheet.css'
    )
)

env.register(
    'css_clockin',
    assets.Bundle(
        'clockin.scss',
        filters='scss',
        output='_gen/css_clockin.css'
    )
)

#####################################################################
#  Blueprints
#####################################################################

# Register the API blueprint.
from app.views.api import api
app.register_blueprint(api, url_prefix='/api/v1')


#####################################################################
#  MongoDB
#####################################################################

# MongoDB information
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017

MONGODB_DBNAME = 'Nomong'  # Gnomon, only backwards.

# Mongo Sessions Interface
from sessions import MongoSessionInterface
app.session_interface = MongoSessionInterface(host=MONGODB_HOST, port=MONGODB_PORT, db=MONGODB_DBNAME)

from pymongo import MongoClient
connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
db = connection[MONGODB_DBNAME]

#####################################################################
#  Views
#####################################################################

# Import all the views here
from views import root
