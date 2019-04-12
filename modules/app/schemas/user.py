from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError

user_schema = {
    "type": "object",
    "properties": {
        "uname": {
            "type": "string",
            "maxLength": 20,
            "minLength": 3
        },
        "email": {
            "type": "string",
            "format": "email"
        },
        "password": {
            "type": "string",
            "minLength": 5
        },
        "re_password": {
            "type": "string",
        }
    },
    "required": ["email", "password"],
}


def validate_user(data):
    try:
        validate(data, user_schema)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    if data.get('re_password') and data['re_password'] != data['password']:
        return {'ok': False, 'message': 'Passwords don\'t match !'}

    return {'ok': True, 'data': data}