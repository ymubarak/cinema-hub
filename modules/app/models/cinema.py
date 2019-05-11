from flask import request, jsonify, g, Blueprint
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity)
from repo import mongo, flask_bcrypt, jwt, LOG, USER_TYPES
from app.schemas.movie import validate_movie
from app.schemas.cinema import validate_cinema_edit

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


@bp.route('/editprofile', methods=['POST'])
def edit_profile():
    ''' edit profile'''
    if not g.usermail:
        return jsonify({'ok': True , 'message': 'User not logged. Please login first.'}), 401

    data = validate_cinema_edit(request.get_json())
    if data['ok']:
        user = mongo.db.users.find_one({'email': g.usermail})
        if user and user['type'] == USER_TYPES[2]:
            edit = data['data']
            update = {'$set': {'info': edit['info'], 'location': edit['location']}}
            response = mongo.db.cinemas.update_one({'email': user['email']}, update)
            if response.acknowledged:
                return jsonify({'ok': True, 'message': 'Cinema profile was updated successfully!'}), 200
            else:
                return jsonify({'ok': False, 'message': 'Error during updating cinema profile'}), 400

        msg, err = 'User does not exist !', 400 if not user else 'Unauthorized action: Only cinemas can edit profile!', 401
        return jsonify({'ok': False, 'message': msg}), err

    return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format( data['message'])}), 400



@bp.route('/editmovie', methods=['POST'])
def edit_movie():
    ''' edit profile'''
    if not g.usermail:
        return jsonify({'ok': True , 'message': 'User not logged. Please login first.'}), 401

    data = validate_movie(request.get_json())
    if data['ok']:
        edit = data['data']
        cinema = mongo.db.cinemas.find_one({'email': g.usermail})
        movies_list = cinema.get('movies', [])
        movie_index = -1
        for i, m in enumerate(movies_list):
            if edit['name'] == m['name']:
                movie_index = i
                break
        if movie_index == -1:
            return jsonify({'ok': False, 'message': 'Movie not found!'}), 400
        # edit movie
        movies_list[movie_index] = edit
        response = mongo.db.cinemas.update_one({'email': cinema['email']}, {'$set': {'movies': movies_list}})
        if response.acknowledged:
            return jsonify({'ok': True, 'message': 'Movie information was updated successfully!'}), 200
        else:
            return jsonify({'ok': False, 'message': 'Error during updating movie information'}), 400

    return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format( data['message'])}), 400