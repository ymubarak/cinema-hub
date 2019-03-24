from flask import request, jsonify
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity)
from repo import app, appmongo, flask_bcrypt, jwt, LOG
from app.schemas import validate_user
import logger


@app.route('/totalsales', methods=['POST'])
def view_sales():
    ''' view movie sales '''
    data = request.get_json()
    # if data['since']:
        # mongo.db...
    pass

@app.route('/topcinemas', methods=['POST'])
def top_cinemas():
    ''' show top rated cinema '''
    data = request.get_json()
    # if data['num']:
        # mongo.db...
    pass


@app.route('/faveoredmovies', methods=['GET'])
def faveored_movies():
    ''' show top faveore dmovies '''
    pass