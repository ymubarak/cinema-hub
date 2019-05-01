''' controller and routes for users '''
from flask import request, jsonify, redirect, url_for, render_template, Blueprint, session
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity)
from repo import mongo, flask_bcrypt, jwt, LOG, USER_TYPES
from app.schemas.user import validate_registering_user, validate_logging_user


LOGIN_PAGE = 'auth/login.html'
REGISTER_PAGE = 'auth/register.html'

bp = Blueprint('auth', __name__)

@jwt.unauthorized_loader
def unauthorized_response(callback):
    return jsonify({
        'ok': False,
        'message': 'Missing Authorization Header'
    }), 401


@bp.route('/register', methods=['GET','POST'])
def register():
    ''' register user endpoint '''
    if request.method == 'POST':
        data = validate_registering_user(request.get_json())
        if data['ok']:
            user = data['data']
            existing_user = mongo.db.users.find_one({'email': user['email']})
            if existing_user:
                return jsonify({'ok': False, 'message': 'User email already exists!'}), 400
            # new user -> hash password and store user
            del user['re_password']
            user['password'] = flask_bcrypt.generate_password_hash(
                user['password'])
            user['type'] = USER_TYPES[1]
            response = mongo.db.users.insert_one(user)
            if response.acknowledged == False:
                return jsonify({'ok': False, 'message': 'Registeration failed!: {}'}), 400
            session['usermail'] = user['email']
            return jsonify({'ok': True, 'message': 'User created successfully!'}), 200
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(data['message'])}), 400

    return render_template(REGISTER_PAGE)


@bp.route('/login', methods=['GET','POST'])
def login():
    ''' auth endpoint '''
    if request.method == 'POST':
        data = validate_logging_user(request.get_json())
        if data['ok']:
            logging_user = data['data']
            # check if user email exists
            user = mongo.db.users.find_one({'email': logging_user['email']})
            # LOG.debug(user)
            if user == None: # user doesn't exist
                return jsonify({'ok': False, 'message': 'User not found'}), 401
            # if user exists
            if flask_bcrypt.check_password_hash(user['password'], logging_user['password']):
                del user['password']
                access_token = create_access_token(identity=logging_user)
                refresh_token = create_refresh_token(identity=logging_user)
                user['token'] = access_token
                user['refresh'] = refresh_token
                session['usermail'] = user['email']
                return jsonify({'ok': True, 'data': user}), 200
            else:
                return jsonify({'ok': False, 'message': 'Invalid email or password'}), 401
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(data['message'])}), 400

    return render_template(LOGIN_PAGE)


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@bp.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    ''' refresh token endpoint '''
    current_user = get_jwt_identity()
    ret = {
        'token': create_access_token(identity=current_user)
    }
    return jsonify({'ok': True, 'data': ret}), 200


@bp.route('/user', methods=['GET', 'DELETE', 'PATCH'])
@jwt_required
def user():
    ''' route read user '''
    if request.method == 'GET':
        query = request.args
        data = mongo.db.users.find_one(query, {"_id": 0})
        return jsonify({'ok': True, 'data': data}), 200

    data = request.json()
    if request.method == 'DELETE':
        if data.get('email', None) is not None:
            db_response = mongo.db.users.delete_one({'email': data['email']})
            if db_response.deleted_count == 1:
                response = {'ok': True, 'message': 'record deleted'}
            else:
                response = {'ok': True, 'message': 'no record found'}
            return jsonify(response), 200
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400

    if request.method == 'PATCH':
        if data.get('query', {}) != {}:
            mongo.db.users.update_one(
                data['query'], {'$set': data.get('payload', {})})
            return jsonify({'ok': True, 'message': 'record updated'}), 200
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400
