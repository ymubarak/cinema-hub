from flask import request, jsonify, Blueprint, g
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity)
from repo import mongo, flask_bcrypt, jwt, LOG, USER_TYPES
from app.schemas.cinema import validate_cinema, cinema_schema

bp = Blueprint('admin', __name__)


@bp.route('/registercinema', methods=['POST'])
def register_cinema():
    ''' register user endpoint '''
    if not g.usermail:
        return jsonify({'ok': True , 'message': 'User not logged. Please login first.'}), 401

    data = validate_cinema(request.get_json())
    if data['ok']:
        user = data['data']
        existing_user_email = mongo.db.users.find_one({'email': user['email']})
        if existing_user_email:
            return jsonify({'ok': False, 'message': 'User with this email already exists!'}), 400
        existing_cinema_name = None
        existing_user_name = mongo.db.users.find_one({'uname': user['uname']})
        if existing_user_name and existing_user_name['type'] == USER_TYPES[2]:
            return jsonify({'ok': False, 'message': 'Cinema with this name already exists!'}), 400

        user['password'] = flask_bcrypt.generate_password_hash(
            user['password'])
        user['type'] = USER_TYPES[2]
        # create cinema document
        cinema = dict(cinema_schema)
        cinema['email'] = user['email']
        # add cinema user
        user_response = mongo.db.users.insert_one(user)
        cinema_response = mongo.db.cinemas.insert_one(cinema)
        if user_response.acknowledged == False or cinema_response.acknowledged == False:
            # remove effect of incomplete cinema creation
            mongo.db.users.delete_one({'email': user['email']})
            mongo.db.cinemas.delete_one({'email': user['email']})
            return jsonify({'ok': False, 'message': 'Error during adding cinema!: {}'}), 400
        return jsonify({'ok': True, 'message': 'Cinema created successfully!'}), 200

    return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(data['message'])}), 400


@bp.route('/unregistercinema', methods=['POST'])
def unregister_cinema():
    ''' unregister cinema '''
    if not g.usermail:
        return jsonify({'ok': True , 'message': 'User not logged. Please login first.'}), 401

    data = request.get_json()
    cinema_mail = data.get('email', None)
    if cinema_mail != None:
        user = mongo.db.users.find_one({'email': cinema_mail})
        if user and user['type'] == USER_TYPES[2]:
            users_response = mongo.db.users.delete_one({'email': cinema_mail})
            cinemas_response = mongo.db.cinemas.delete_one({'email': cinema_mail})
            if users_response.deleted_count == 1 and cinemas_response.deleted_count == 1:
                return jsonify({'ok': True, 'message': 'Cinema is deleted successfully!'}), 200
            return jsonify({'ok': False, 'message': 'Error during deleting the cinema records'}), 400
        else:
            return jsonify({'ok': False, 'message': 'No cinema user with this email'}), 400

    return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(cinema_mail)}), 400