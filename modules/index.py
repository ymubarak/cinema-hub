""" index file for REST APIs using Flask """
import sys
import requests
from flask import jsonify, request, make_response, send_from_directory
from app import app, LOG

DIR = 'templates'

@app.errorhandler(404)
def not_found(error):
    """ error handler """
    LOG.error(error)
    return send_from_directory(DIR, '404.html')
    # return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/')
def index():
    """ static files serve """
    return send_from_directory(DIR, 'index.html')


@app.route('/<path:path>')
def static_proxy(path):
    """ static folder serve """
    file_name = path.split('/')[-1]
    dir_name = os.path.join(DIR, '/'.join(path.split('/')[:-1]))
    return send_from_directory(dir_name, file_name)


if __name__ == '__main__':
    LOG.info('running environment: %s', os.environ.get('ENV'))
    app.config['DEBUG'] = os.environ.get('ENV') == 'development' # Debug mode if development env
    PORT= sys.argv[1] if len(sys.argv)>1 else 5000
    app.run(host='0.0.0.0', port=int(PORT)) # Run the app