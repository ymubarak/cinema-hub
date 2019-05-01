""" index file for REST APIs using Flask """
import os
import sys
import requests
import logger
from flask import jsonify, redirect, url_for, send_from_directory, render_template, session, g
from app import create_app
import repo

VIEW_DIR = 'templates'
ERROR_PAGE = '404.html'
HOME_PAGE = 'index.html'

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
os.environ.update({'ROOT_PATH': ROOT_PATH})
sys.path.append(os.path.join(ROOT_PATH, 'modules'))

# create the flask object
app = create_app()
# Create a logger object to log the info and debug
LOG = logger.get_root_logger(os.environ.get(
    'ROOT_LOGGER', 'root'), filename=os.path.join(os.environ.get('ROOT_PATH'), 'output.log'))

# initialize repo
repo.init(app, LOG)

# registers blueprints
from app.controllers import auth
from app.models import admin
from app.models import cinema
from app.models import user
from app.models import reports

app.register_blueprint(auth.bp)
app.register_blueprint(admin.bp)
app.register_blueprint(cinema.bp)
app.register_blueprint(user.bp)
app.register_blueprint(reports.bp)

@app.errorhandler(404)
def not_found(error):
    """ error handler """
    LOG.error(error)
    return send_from_directory('templates' , ERROR_PAGE)
    # return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/')
def index():
    """ static files serve """
    if g.usermail:
        return render_template(HOME_PAGE)
    else:
        return redirect(url_for('auth.login'))

# check user is logged in before any request
@app.before_request
def load_logged_in_user():
    g.usermail  = session.get('usermail')


@app.route('/<path:path>')
def static_proxy(path):
    """ static folder serve """
    file_name = path.split('/')[-1]
    dir_name = os.path.join(VIEW_DIR, '/'.join(path.split('/')[:-1]))
    return send_from_directory(dir_name, file_name)


if __name__ == '__main__':
    LOG.info('running environment: %s', os.environ.get('ENV'))
    app.config['DEBUG'] = os.environ.get('ENV') == 'development' # Debug mode if development env
    PORT= sys.argv[1] if len(sys.argv)>1 else 5000
    app.run(host='0.0.0.0', port=int(PORT)) # Run the app
