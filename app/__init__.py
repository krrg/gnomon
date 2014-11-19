from flask import Flask
from flask.ext import assets
import os

app = Flask(__name__)
env = assets.Environment(app)

# Tell flask-assets where to look for the sass/scss files.

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


# Import all the views here
from views import root