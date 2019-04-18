from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError

MOVIE_GENRES = ["Action", "Adventure", "Comedy", "Crime", "Mystery", "Drama", "Fantasy", "Historical",
             "Horror", "Political", "Romance", "Saga", "Satire", "Science", "fiction", "Social", "Thriller"]
SORTING_METHODS = ['Latest', 'Cheapest']


movie_schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
        },
        "genre": {
            "type": "string",
            "enum": MOVIE_GENRES
        },
        "director": {
            "type": "string",
        },
        "price": {
            "type": "number",
             "minimum": 0
        },
        "starting_date": {
            "type": "string",
            "format": "date"
        }
    },
    "required": ["name", "genre", "director", "price", "starting_date"],
}

movie_search_schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
        },
        "genre": {
            "type": "string",
            "enum": MOVIE_GENRES + ["Any"]
        },
        "sortby": {
            "type": "string",
            "enum": SORTING_METHODS
        },
    },
    "required": ["genre", "sortby", "director", "price", "starting_date"],
}

def validate_movie(data):
    try:
        validate(data, movie_schema)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}

def validate_search_query(data):
    pass