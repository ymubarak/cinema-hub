from flask import request, jsonify, g
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity)
from repo import app, appmongo, flask_bcrypt, jwt, LOG
from app.schemas import validate_movie
import logger


@app.route('/addmovie', methods=['POST'])
def add_movie():
    ''' add movie'''
    data = validate_movie(request.get_json())
    if data['ok']:
        movie = data['data']
        cinema = mongo.db.cinemas.find_one({'_id': g.user['_id']})
        for m in cinema['movies']
            if movie['name'] == m['name']:
                return jsonify({'ok': False, 'message': 'Movie '{}'already exists.'.format(movie['name'])}), 400
        # add movie
        mongo.db.cinemas.
        return jsonify({'ok': True, 'message': 'Movie added successfully!'}), 200
    else:
        return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(data['message'])}), 400

@app.route('/removemovie', methods=['DELETE'])
def remove_movie():
    ''' remove movie '''
    movie_name = request.form['name']
    if movie_name:
        cinema = mongo.db.cinemas.find_one({'_id': g.user['_id']})
        for m in cinema['movies']
            if movie_name == m['name']:
                 # remove movie
                 return jsonify({'ok': True, 'message': 'Movie added successfully!'}), 200
        return jsonify({'ok': False, 'message': 'Movie '{}' does not exists.'.format(movie_name)}), 400
    else:
        return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(movie_name)}), 400

@app.route('/updaterate', methods=['POST'])
def update_rate():
    ''' update rate '''
    pass
