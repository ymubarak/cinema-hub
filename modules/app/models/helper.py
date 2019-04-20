from app.schemas.movie import validate_search_query, MOVIE_SORTING_METHODS
from app.schemas.cinema import validate_search_cinema, CINEMA_SORTING_METHODS
from math import pi, pow, sin, cos, sqrt, atan2
# set of helper methods

def calc_total_rate(rate):
    summation = (rate['1']+rate['2']+rate['3']+rate['4']+rate['5'])
    weighted_sum = (rate['1']+rate['2']*2+rate['3']*3+rate['4']*4+rate['5']*5)
    return 0 if summation==0 else weighted_sum/summation


#calculate haversine distance for linear distance
def calc_distance(loc1, loc2):
    # {'latitude': x, 'longitude': y}
    lat1 = loc1['latitude']
    long1 = loc1['longitude']
    lat2 = loc2['latitude']
    long2 = loc2['longitude']

    d2r = pi/180.0
    dlong = (long2 - long1) * d2r;
    dlat = (lat2 - lat1) * d2r;
    a = pow(sin(dlat/2.0), 2) + cos(lat1*d2r) * cos(lat2*d2r) * pow(sin(dlong/2.0), 2);
    c = 2 * atan2(sqrt(a), sqrt(1-a));
    distance = 6367 * c;

    return abs(distance);


def validate_rate(rate):
    try:
        return 1 <= int(rate) <= 5
    except:
        return False


def sort_cinemas(cinemas, query):
    assert validate_search_cinema(query) , "Invalid search query"
    # ['Rate', 'Nearest', 'Alphabetical']
    sort_method = query['sortby']
    if sort_method == 'Rate':
        cinemas = sorted(cinemas, key = lambda c: calc_total_rate(c['rate']), reverse=True)
    elif sort_method == 'Nearest':
        cinemas = sorted(cinemas, key = lambda c: calc_distance(c['location'], query['location']))
    elif sort_method == 'Alphabetical':
        cinemas = sorted(cinemas, key = lambda c: c['uname'])

    return cinemas


def sort_movies(movies, sort_method):
    assert sort_method in MOVIE_SORTING_METHODS, "Sorting method not recognized"
    # ['Latest', 'Oldest', 'Alphabetical', 'Cheapest']
    if sort_method == 'Latest':
        movies = sorted(movies, key = lambda m: m['starting_date'], reverse=True)
    elif sort_method == 'Oldest':
        movies = sorted(movies, key = lambda m: m['starting_date'])
    elif sort_method == 'Alphabetical':
        movies = sorted(movies, key = lambda m: m['name'])
    elif sort_method == 'Cheapest':
        movies = sorted(movies, key = lambda m: m['price'])

    return movies
