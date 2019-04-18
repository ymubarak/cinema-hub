from .schema import *

NAME_MAX_LENGTH = 20
NAME_MIN_LENGTH = 3
PASSWORD_MIN_LENGTH = 5

registeration_schema = {
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
        },
        "re_password": {
            "type": "string",
        }
    },
    "required": ["uname", "email", "password", "re_password"],
}

login_schema = {
    "type": "object",
    "properties": {
        "email": {
            "type": "string",
            "format": "email"
        },
        "password": {
            "type": "string",
            "minLength": PASSWORD_MIN_LENGTH
        }
    },
    "required": ["email", "password"],
}

def validate_registering_user(user_data):
    result = validate_schema(user_data, registeration_schema)
    if not result['ok']:
        return result
    elif user_data['re_password'] != user_data['password']:
        return {'ok': False, 'message': 'Passwords don\'t match !'}

    return result


def validate_logging_user(user_data):
    return validate_schema(user_data, login_schema)
