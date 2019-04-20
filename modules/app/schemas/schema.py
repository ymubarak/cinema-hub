from jsonschema import validate, FormatChecker
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError

def validate_schema(data, schema):
    try:
        validate(data, schema, format_checker=FormatChecker())
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}