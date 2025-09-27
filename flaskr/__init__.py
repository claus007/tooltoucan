import os

from flask import Flask
from flask import render_template

def create_app():
    global app
    # create and configure the app
    app = Flask("ToolToucan", instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'   )

create_app()

# a simple page that says hello
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/license')
def license():
    return render_template('license.html')
