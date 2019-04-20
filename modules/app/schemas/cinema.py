from .schema import *
import re

NAME_MAX_LENGTH = 20
NAME_MIN_LENGTH = 3
PASSWORD_MIN_LENGTH = 5
WEBSITE = "cinemahub.com"
CINEMA_SORTING_METHODS = ['Rate', 'Nearest', 'Alphabetical']


cinema_schema = {
    "email": ""
    ,
    "location": ""
    ,
    "cover": ""
    ,
    "movies": []
    ,
    "info": ""
    ,
    "rate": {'1': 0, '2': 0,'3': 0,'4': 0, '5': 0}
}

cinema_edit_schema = {
    "type": "object",
    "required": ["location", "info"],
    "properties": {
        "cover": {
            "type": "string",
        },
        "location": {
            "title": "Longitude and Latitude Values",
            "description": "A geographical coordinate.",
            "required": [ "latitude", "longitude" ],
            "type": "object",
            "properties": {
                "latitude": {
                  "type": "number",
                  "minimum": -90,
                  "maximum": 90
                },
                "longitude": {
                  "type": "number",
                  "minimum": -180,
                  "maximum": 180
                }
            }
        },
        "info": {
            "type": "string",
            "maxLength": 150
        },
    },
}

cinema_creation_schema = {
    "type": "object",
    "properties": {
        "uname": {
            "type": "string",
            "maxLength": NAME_MAX_LENGTH,
            "minLength": NAME_MIN_LENGTH
        },
        "email": {
            "type": "string",
            "format": "email"
        },
        "password": {
            "type": "string",
            "minLength": PASSWORD_MIN_LENGTH
        }
    },
    "required": ["uname", "email", "password"],
}

cinema_search_schema = {
    "type": "object",
    "required": ["sortby"],
    "properties": {
        "name": {
            "type": "string",
        },
        "location": {
            "title": "Longitude and Latitude Values",
            "description": "A geographical coordinate.",
            "required": [ "latitude", "longitude" ],
            "type": "object",
            "properties": {
                "latitude": {
                  "type": "number",
                  "minimum": -90,
                  "maximum": 90
                },
                "longitude": {
                  "type": "number",
                  "minimum": -180,
                  "maximum": 180
                }
            }
        },
        "sortby": {
            "type": "string",
            "enum": CINEMA_SORTING_METHODS
        },
    },
}


def validate_cinema(cinema_user):
    result = validate_schema(cinema_user, cinema_creation_schema)
    if not result['ok']:
        return result
    # validate cinema name
    pattern = "(.+@{})$".format(WEBSITE)
    if not re.search(pattern, cinema_user['email']):
        return {'ok': False,
        'message': 'Cinema email must be tied to cinemahub.com (Ex. a valid email may be name@cinemahub.com'}

    return result

def validate_search_cinema(search_query):
    result = validate_schema(search_query, cinema_search_schema)
    if not result['ok']:
        return result
    # check location if sort method is nearest
    if search_query['sortby' == 'Nearest'] and search_query.get('location', None) == None:
        return {'ok': False, 'message': 'Sorting by \'Nearest\' requires the location field'}

    return result

def validate_cinema_edit(edit_data):
    result = validate_schema(edit_data, cinema_edit_schema)
    if not result['ok']:
        return result
    # check location if sort method is nearest
    # if edit_data.get('cover', None):
    #     return {'ok': False, 'message': 'Sorting by \'Nearest\' requires the location field'}

    return result