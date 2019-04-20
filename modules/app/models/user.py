from flask import request, jsonify, Blueprint, g
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity)
from repo import mongo, flask_bcrypt, jwt, LOG, USER_TYPES
from app.schemas.movie import validate_search_query
from app.schemas.cinema import validate_search_cinema
from app.models.helper import validate_rate, sort_cinemas, sort_movies
import re


RESTRICT_USER = True # only allow regular users to have a favorite list

bp = Blueprint('user', __name__)

@bp.route('/ratecinema', methods=['POST'])
def rate_cinema():
    ''' update rate '''
    if not g.usermail:
        return jsonify({'ok': True , 'message': 'User not logged. Please login first.'}), 401

    data = request.get_json()
    cinema_name, rate = data.get('cinema_name', None), data.get('rate', None)
    if cinema_name and validate_rate(rate):
        user = mongo.db.users.find_one({'uname': cinema_name})
        if user and user['type'] == USER_TYPES[2]:
            cinema = mongo.db.cinemas.find_one({'email': user['email']})
            cinema_rate = cinema['rate']
            cinema_rate[rate] += 1
            response = mongo.db.cinemas.update_one({'email': cinema['email']}, {'$set': {'rate': cinema_rate}})
            if response.acknowledged:
                return jsonify({'ok': True, 'message': 'Cinema rate was updated successfully!'}), 200
            else:
                return jsonify({'ok': False, 'message': 'Error during updating cinema rate'}), 400

        return jsonify({'ok': False, 'message': 'Cinema does not exist !'}), 400

    return jsonify({'ok': False,
     'message': 'Bad request parameters: "Cinema : {}", "rate: {}"'.format(cinema_name, rate)}), 400


@bp.route('/getcinemarate', methods=['POST'])
def get_cinema_rate():
    ''' add movie'''
    if not g.usermail:
        return jsonify({'ok': True , 'message': 'User not logged. Please login first.'}), 401

    data = request.get_json()
    cinema_name = data.get('cinema_name', None)
    if cinema_name:
        cinema = mongo.db.users.find_one({'uname': cinema_name})
        if cinema and cinema['type'] == USER_TYPES[2]:
            cinema = mongo.db.cinemas.find_one({'email': cinema['email']})
            rate = cinema.get('rate', [])
            return jsonify({'ok': True, 'data': rate}), 200

        return jsonify({'ok': False, 'message': 'Cinema does not exist !'}), 400

    return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(cinema_name)}), 400


@bp.route('/getcinemamovies', methods=['POST'])
def get_movie():
    ''' add movie'''
    if not g.usermail:
        return jsonify({'ok': True , 'message': 'User not logged. Please login first.'}), 401

    data = request.get_json()
    cinema_name = data.get('cinema_name', None)
    if cinema_name:
        cinema = mongo.db.users.find_one({'uname': cinema_name})
        if cinema and cinema['type'] == USER_TYPES[2]:
            cinema = mongo.db.cinemas.find_one({'email': cinema['email']})
            movies = cinema.get('movies', [])
            return jsonify({'ok': True, 'data': movies}), 200

        return jsonify({'ok': False, 'message': 'Cinema does not exist !'}), 400

    return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(cinema_name)}), 400


@bp.route('/addtofavorite', methods=['POST'])
def add_to_favorite():
    ''' add movie to favorite '''
    if not g.usermail:
       return jsonify({'ok': True , 'message': 'User not logged. Please login first.'}), 401

    data = request.get_json()
    cinema_name, movie_name = data.get('cinema_name', None), data.get('movie_name', None)
    if cinema_name and movie_name:
        user = mongo.db.users.find_one({'email': g.usermail})
        if user and user['type'] == USER_TYPES[2]:
            favorites = user.get('favorite', [])
            favorites.append({'movie_name': movie_name, 'cinema_name': cinema_name})
            response = mongo.db.users.update_one({'email': user['email']}, {'$set': {'favorite' , favorites}})
            if response.acknowledged:
                return jsonify({'ok': True, 'message': 'Movie was add to favorites list successfully!'}), 200
            else:
                return jsonify({'ok': False, 'message': 'Error during updating adding movie to favorites'}), 400

        return jsonify({'ok': False, 'message': 'User does not exist !'}), 401

    return jsonify({'ok': False, \
         'message': 'Bad request parameters: "Cinema : {}", "Movie: {}"'.format(cinema_name, movie_name)}), 400


@bp.route('/favorites', methods=['GET'])
def favorite_movies():
    ''' show top faveored movies '''
    if not g.usermail:
        return jsonify({'ok': True , 'message': 'User not logged. Please login first.'}), 401

    user = mongo.cinemahub.users.find_one({'email' : g.usermail})
    if user:
        if RESTRICT_USER and user['type'] != USER_TYPES[1]:
            return jsonify({'ok': False, 'message': 'Favorite list is not provided for this user'}), 400

        return jsonify({'ok': True, 'data': user.get('favorite', [])}), 200
    return jsonify({'ok': False, 'message': 'User does not exist. Please sign up first.'}), 401


@bp.route('/profile', methods=['GET'])
def profile():
    ''' open profile page '''
    if not g.usermail:
        return jsonify({'ok': True , 'message': 'User not logged. Please login first.'}), 401

    current_user = mongo.db.users.find_one({"email": g.usermail})
    if current_user:
        del current_user['password']
        if current_user['type'] == USER_TYPES[0]: # Admin
            return jsonify({'ok': True, 'data': current_user}), 200
        elif current_user['type'] == USER_TYPES[1]: # Regular user
            return jsonify({'ok': True, 'data': current_user}), 200
        else: # Cinema
            cinema = mongo.db.cinemas.find_one({"email": current_user['email']})
            data = {**current_user, **cinema}
            return jsonify({'ok': True, 'data': data}), 200

    return jsonify({'ok': False, 'message': 'User does not exist. Please sign up first.'}), 401


@bp.route('/searchcinema', methods=['POST'])
def search_cinema():
    ''' search for a specific cinema '''
    data = validate_search_cinema(request.get_json())
    if data['ok']:
        query = data['data']
        cinemas = []
        if query['name']:
            pattern = '/.*{}.*/'.format(query['name'])
            cinemas = mongo.db.cinemas.find({'name': { '$regex': pattern }})
        else:
            cinemas = mongo.db.cinemas.find()
        cinemas = sort_cinemas(cinemas,  query)
        return jsonify({'ok': True, 'data': cinemas}), 200

    return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(data['message'])}), 400


@bp.route('/searchmovie', methods=['POST'])
def search_movie():
    ''' search for a specific movie '''
    data = validate_search_query(request.get_json())
    if data['ok']:
        query = data['data']
        movies = []
        cinemas = []
        if query['cinemaname']:
            cinema_user = mongo.db.cinemas.find_one({'uname': query['cinemaname']})
            cinemas  = mongo.db.cinemas.find({'email': cinema_user['email']})
        else:
            cinemas = mongo.db.cinemas.find()
        for c in cinemas:
            for m in c['movies']:
                match_genre = query['genre'] in ['All' , m['genre']]
                pattern = '/.*{}.*/'.format(query['name']) if query['name'] else ''
                match_name = re.search(pattern, m['name']) if query['name'] else True
                if match_name and match_genre:
                    movies.append(m)

        movies = sort_movies(movies,  query['sortby'])
        return jsonify({'ok': True, 'data': movies}), 200

    return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(data['message'])}), 400