import random
from pymongo import MongoClient
import flask_bcrypt

DB_URL = 'mongodb://localhost:27017/'

cinemas_users = [
    {'uname': 'Metro', 'email': 'metro@cinemahub.com', "type" : "C", 'password': '123456'},
    {'uname': 'Amir', 'email': 'amir@cinemahub.com', "type" : "C", 'password': '123456'},
    {'uname': 'Ferial', 'email': 'ferial@cinemahub.com', "type" : "C", 'password': '123456'},
    {'uname': 'San', 'email': 'san@cinemahub.com', "type" : "C", 'password': '123456'},
    {'uname': 'Geleem', 'email': 'geleem@cinemahub.com', "type" : "C", 'password': '123456'},
    {'uname': 'Grand', 'email': 'grand@cinemahub.com', "type" : "C", 'password': '123456'},
    {'uname': 'Vox', 'email': 'vox@cinemahub.com', "type" : "C", 'password': '123456'},
    {'uname': 'Carefour', 'email': 'carefour@cinemahub.com', "type" : "C", 'password': '123456'},
    {'uname': 'Citycentre', 'email': 'citycentre@cinemahub.com', "type" : "C", 'password': '123456'},
    {'uname': 'Setrand', 'email': 'setrand@cinemahub.com', "type" : "C", 'password': '123456'}
    ]

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

movie_schema ={'name': '', 'genre': [], 'director': ' ', 'price': 0.0, 'starting_date': '', 'poster': ''}
movies = []
with open('movies.tsv', 'r') as f:
    movies = f.readlines()


# FNAMES = ["Ruben", "Knox", "Taylor", "Garland", "Bernadine", "Evangeline", "Denton", "Mercy", "Garland", "Neil", "Lowell"]
# LNAMES = ["Fleischer", "Oakley", "Stephen", "Esther", "Dominic", "Granville", "Denver", "Fern", "Jarod", "Calton"]

db = MongoClient(DB_URL)
drop_db = lambda x: db.drop_database(x)
create_db = lambda x: db[x]

def create_admin(db):
    # defining a params dict for the parameters to be sent to the API
    params = {'uname': 'admin', 'email': 'admin@cinemahub.com', 'password': '123456', 'type': 'A'}
    params['password'] = flask_bcrypt.generate_password_hash(params['password'])
    response = db.users.insert_one(params)
    if response.acknowledged:
        print("create_admin: passed")
    else:
        print("create_admin: failed")
    print()

def create_cinemas(db):
    for cu in cinemas_users:
        cu['password'] = flask_bcrypt.generate_password_hash(cu['password'])
    users_response = db.users.insert(cinemas_users)

    for cu in cinemas_users:
        cs = dict(cinema_schema)
        cs['email'] = cu['email']
        cinema_response = db.cinemas.insert_one(cs)
        if not cinema_response.acknowledged:
            print("create_cinema: failed")
            return
    print("create_cinemas: passed")



def create_movie():
    info = random.choice(movies)
    movies.remove(info)
    info = info.split('\t')

    movie = dict(movie_schema)
    movie['name'] = info[0]
    movie['genre'] = list(map(lambda x: x.strip(), info[1].split(',')))
    movie['director'] = info[2]
    movie['poster'] = info[4]

    year = info[3]
    month = str(random.choice(range(1,13)))
    month = month if len(month)==2 else '0'+month
    day = str(random.choice(range(1,29)))
    day = day if len(day)==2 else '0'+day
    movie['starting_date'] = year+'-'+month+'-'+day

    movie['price'] = random.choice(range(10,100)) + random.choice(range(1,100))/10
    return movie


def create_movies(db):
    movies_per_cinema = len(movies)//len(cinemas_users)
    for cu in cinemas_users:
        i = 0
        while i < movies_per_cinema:
            i += 1
            cinema = db.cinemas.find_one({'email': cu['email']})
            movies_list = cinema.get('movies', [])
            movie = create_movie()
            movies_list.append(movie)

            response = db.cinemas.update_one({'email': cinema['email']}, {'$set': {'movies': movies_list}})
            if not response.acknowledged:
                print("create_movies: failed")
                return
    print("create_movies: passed")


def main():
    drop_db('cinemahub')
    db = create_db('cinemahub')
    create_admin(db)
    create_cinemas(db)
    create_movies(db)


if __name__ == '__main__':
    main()
