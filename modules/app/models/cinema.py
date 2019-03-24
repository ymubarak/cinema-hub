from flask import request, jsonify
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity)
from repo import app, appmongo, flask_bcrypt, jwt, LOG
from app.schemas import validate_moive
import logger


@app.route('/addmovie', methods=['POST'])
def add_movie():
    ''' add movie'''
    data = validate_moive(request.get_json())
    if data['ok']:
        data = data['data']
        pass
    pass

@app.route('/removemovie', methods=['DELETE'])
def remove_movie():
    ''' remove movie '''
    pass

@app.route('/updaterate', methods=['DELETE'])
def update_rate():
    ''' update rate '''
    pass
