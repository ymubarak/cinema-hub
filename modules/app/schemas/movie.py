from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError

movie_schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
        },
        "genre": {
            "type": "string",
            "enum": ["Action", "Adventure", "Comedy", "Crime", "Mystery", "Drama", "Fantasy", "Historical",
             "Horror", "Political", "Romance", "Saga", "Satire", "Science", "fiction", "Social", "Thriller"]
        },
        "director": {
            "type": "string",
        }
        "price": {
            "type": "number",
        }
        "starting_date": {
            "type": "date",
        }
    },
    "required": ["name", "genre", "director", "price", "starting_date"],
}


def validate_movie(data):
    try:
        validate(data, movie_schema)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}