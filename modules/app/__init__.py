''' flask app with mongo '''
import os
import sys
import json
import datetime
from bson.objectid import ObjectId
from flask import Flask

DB_URL = 'mongodb://localhost:27017/cinemahub'
APP_SECRET_KEY = "cdsrytrjytdgffdssda4875"
JWT_SECRET_KEY = "secKeyJWT010"

class JSONEncoder(json.JSONEncoder):
    ''' extend json-encoder class'''
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = APP_SECRET_KEY
    # add mongo url to flask config, so that flask_pymongo can use it to make connection
    app.config['MONGO_URI'] = DB_URL
    app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)

    # app.config.from_mapping(
    #     SECRET_KEY='dev',
    #     DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    # )

    # use the modified encoder class to handle ObjectId & datetime object while jsonifying the response.
    app.json_encoder = JSONEncoder

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app



