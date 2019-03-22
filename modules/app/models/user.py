from flask import request, jsonify
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity)
from app import app, mongo, flask_bcrypt, jwt, LOG
from app.schemas import validate_user
import logger


@app.route('/ratecinema', methods=['POST'])
def rate_cinema():
    ''' rate cinema '''
    pass

@app.route('/searchmovie', methods=['POST'])
def search_movie():
    ''' search for a specific movie '''
    data = request.get_json()
    pass

@app.route('/addtofavorite', methods=['POST'])
def add_to_favorite():
    ''' add movie to favorite '''
    pass
