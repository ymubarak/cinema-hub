from .schema import *

MOVIE_GENRES = ["Action", "Adventure", "Animation", "Biography", "Comedy", "Crime", "Documentary", "Mystery", "Drama",
 "Fantasy", "Historical", "Horror", "Political", "Romance", "Saga", "Satire", "Science", "fiction", "Social", "Thriller", "Western"]
MOVIE_SORTING_METHODS = ['Latest', 'Oldest', 'Alphabetical', 'Cheapest']


movie_schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
        },
        "poster": {
            "type": "string",
        },
        "genre": {
            "type": "array",
            "items": {
                "type": "string",
                "enum": MOVIE_GENRES
            }
        },
        "director": {
            "type": "string",
        },
        "price": {
            "type": "number",
             "minimum": 0.0
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
        "moviename": {
            "type": "string",
        },
        "cinemaname": {
            "type": "string",
        },
        "genre": {
            "type": "string",
            "enum": MOVIE_GENRES + ["All"]
        },
        "sortby": {
            "type": "string",
            "enum": MOVIE_SORTING_METHODS
        },
    },
    "required": ["genre", "sortby"],
}

def validate_movie(movie_data):
    return validate_schema(movie_data, movie_schema)


def validate_search_query(search_query):
    return validate_schema(search_query, movie_search_schema)