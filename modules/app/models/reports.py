from flask import request, jsonify, g, Blueprint
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity)
from repo import app, mongo, flask_bcrypt, jwt, LOG

bp = Blueprint('reports', __name__)

def cal_total_rate(rate):
    summation = (rate['1']+rate['2']+rate['3']+rate['4']+rate['5'])
    weighted_sum = (rate['1']+rate['2']*2+rate['3']*3+rate['4']*4+rate['5']*5)
    return 0 if summation==0 else weighted_sum/summation


@bp.route('/topcinemas', methods=['POST'])
def top_cinemas():
    ''' show top rated cinema '''
    if not g.usermail:
        return jsonify({'ok': True , 'message': 'User not logged. Please login first.'}), 401

    top_k = request.get_json().get('num', None)
    if top_k:
        cinemas = mongo.db.cinemas.find()
        cinemas_rates = []
        for c in cinemas:
            total_rate = cal_total_rate(c['rate'])
            user = mongo.db.users.find_one({'email': c['email']})
            cinemas_rates.append({'name': user['uname'], 'rate':total_rate})

        cinemas_rates = sorted(cinemas_rates, key = lambda x: x['rate'], reverse=True)
        limit = min(top_k, len(cinemas_rates))
        return jsonify({'ok': True, 'data': cinemas_rates[:limit]}), 200
    else:
        return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(top_k)}), 400


@bp.route('/favorites', methods=['GET'])
def favorite_movies():
    ''' show top faveored movies '''
    if not g.usermail:
        return jsonify({'ok': True , 'message': 'User not logged. Please login first.'}), 401

    user = mongo.cinemahub.users.find_one({'email' : g.usermail})
    return jsonify({'ok': True, 'data': user.get('favorite', [])}), 200