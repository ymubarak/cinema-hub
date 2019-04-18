from .schema import *
import re

NAME_MAX_LENGTH = 20
NAME_MIN_LENGTH = 3
PASSWORD_MIN_LENGTH = 5
WEBSITE = "cinemahub.com"

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

#
cinema_schema = {
    "email": ""
    ,
    "location": ""
    ,
    "cover": ""
    ,
    "movies": []
    ,
    "rate": {'1': 0, '2': 0,'3': 0,'4': 0, '5': 0}
}


def validate_cinema(cinema_user):
    result = validate_schema(cinema_user, cinema_creation_schema)
    if not result['ok']:
        return result
    pattern = "(.+@{})$".format(WEBSITE)
    if not re.search(pattern, cinema_user['email']):
        return {'ok': False,
        'message': 'Cinema email must be tied to cinemahub.com (Ex. a valid email may be name@cinemahub.com'}

    return result