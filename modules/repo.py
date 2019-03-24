from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_pymongo import PyMongo

LOG = None
app = None
mongo = None
flask_bcrypt = None
jwt = None

def init(application, logger):
	global mongo, flask_bcrypt, jwt, LOG
	if application:
		app = application
		LOG = logger
		mongo = PyMongo(app)
		flask_bcrypt = Bcrypt(app)
		jwt = JWTManager(app)