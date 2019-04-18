from flask import request, jsonify, g, Blueprint
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity)
from repo import mongo, flask_bcrypt, jwt, LOG, USER_TYPES
from app.schemas.movie import validate_movie


bp = Blueprint('cinema', __name__)

@bp.route('/addmovie', methods=['POST'])
def add_movie():
    ''' add movie'''
    if not g.usermail:
        return jsonify({'ok': True , 'message': 'User not logged. Please login first.'}), 401

    data = validate_movie(request.get_json())
    if data['ok']:
        movie = data['data']
        cinema = mongo.db.cinemas.find_one({'email': g.usermail})
        movies_list = cinema.get('movies', [])
        for m in movies_list:
            if movie['name'] == m['name']:
                return jsonify({'ok': False, 'message': 'Movie \'{}\' already exists.'.format(movie['name'])}), 400
        # add movie
        movies_list.append(movie)
        response = mongo.db.cinemas.update_one({'email': cinema['email']}, {'$set': {'movies': movies_list}})
        if response.acknowledged:
            return jsonify({'ok': True, 'message': 'Movie added successfully!'}), 200
        else:
            return jsonify({'ok': False, 'message': 'Error during adding movie'}), 400

    return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(data['message'])}), 400


@bp.route('/removemovie', methods=['DELETE'])
def remove_movie():
    ''' remove movie '''
    if not g.usermail:
        return jsonify({'ok': True , 'message': 'User not logged. Please login first.'}), 401

    data = request.get_json()
    movie_name = data.get('movie_name', None)
    if movie_name:
        cinema = mongo.db.cinemas.find_one({'email': g.usermail})
        movies_list = cinema.get('movies', [])
        index = -1
        for i, movie in enumerate(movies_list):
            if movie_name == movie['name']:
                index = i
                break
        if index == -1:
            return jsonify({'ok': False, 'message': 'Movie \'{}\' does not exists.'.format(movie_name)}), 400
        # remove movie
        movies_list.pop(index)
        response = mongo.db.cinemas.update_one({'email': cinema['email']}, {'$set': {'movies': movies_list}})
        if response.acknowledged:
            return jsonify({'ok': True, 'message': 'Movie removed successfully!'}), 200
        else:
            return jsonify({'ok': False, 'message': 'Error during removing movie'}), 400

    return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(movie_name)}), 400