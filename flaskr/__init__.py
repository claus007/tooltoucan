import os

from flask import Flask
from flask import render_template
from flaskr.db_con import connect_to_database;
from flaskr.navigation import Navigation;

navigation=None

def create_app():
    global app
    # create and configure the app
    app = Flask("ToolToucan", instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'   )
    success, error, connection = db_con.connect_to_database()
    if success==False:
        print(f"Database connection failed with error: {error}")
        app.config['db_connection'] = None
    else:
        app.config['db_connection'] = connection
        global navigation
        navigation = Navigation().read(connection)
        
create_app()

# a simple page that says hello
@app.route('/')
def index():
    return render_template('index.html',navigation=navigation)

@app.route('/license')
def license():
    return render_template('license.html',navigation=navigation)
