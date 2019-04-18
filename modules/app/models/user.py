from flask import request, jsonify, Blueprint, g
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity)
from repo import mongo, flask_bcrypt, jwt, LOG, USER_TYPES

bp = Blueprint('user', __name__)

def validate_rate(rate):
    try:
        return 1 <= int(rate) <= 5:
    except:
        return False


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


@bp.route('/getmovies', methods=['POST'])
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
        cinema = mongo.db.users.find_one({'uname': cinema_name})
        if cinema and cinema['type'] == USER_TYPES[2]:
            favorites = user.get('favorite', [])
            favorites.append()
            cinema = mongo.db.cinemas.find_one({'email': user['email']})
            cinema_rate = cinema['rate']
            cinema_rate[rate] += 1
            response = mongo.db.cinemas.update_one({'email': cinema['email']}, {'$set': {'rate' , cinema_rate}})
            if response.acknowledged:
                return jsonify({'ok': True, 'message': 'Cinema rate was updated successfully!'}), 200
            else:
                return jsonify({'ok': False, 'message': 'Error during updating cinema rate'}), 400

        return jsonify({'ok': False, 'message': 'Cinema does not exist !'}), 400

    return jsonify({'ok': False, \
         'message': 'Bad request parameters: "Cinema : {}", "Movie: {}"'.format(cinema_name, movie_name)}), 400


@bp.route('/profile', methods=['GET'])
def profile():
    ''' open profile page '''
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

    return jsonify({'ok': False, 'message': 'User not logged. Please login first.'}), 401


@bp.route('/searchcinema', methods=['POST'])
def search_cinema():
    ''' search for a specific cinema '''
    data = request.get_json()
    pass

@bp.route('/searchmovie', methods=['POST'])
def search_movie():
    ''' search for a specific movie '''
    data = request.get_json()
    pass
