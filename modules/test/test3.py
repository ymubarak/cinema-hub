# importing the requests library
import requests

# api-endpoint
URL = "http://0.0.0.0:5000/"
HEADERS = {
    'type': 'POST',
    'contentType': "application/json; charset=utf-8",
    'dataType': 'json',
}

def get_movies(cinema_name):
	'''get cinema movies'''
	params = {'email': 'metro@cinemahub.com', 'password': '123456'}
	# sending get request and saving the response as response object
	login_url = URL + "login"
	rs = requests.session()
	login_response = rs.post(url = login_url, headers=HEADERS, json=params)

	params_2 = {
	 'cinema_name': cinema_name,
	 }
	# sending get request and saving the response as response object
	url = URL + "getcinemamovies"
	response = rs.post(url = url, headers=HEADERS, json=params_2)
	# extracting data in json format
	data = response.json()
	print('response:\n', data['data'])
	if data['ok']== True and response.status_code == 200:
		print("Passed")
	else:
		print("Failed")
	print()


def search_movie(genre, sortby, moviename=None, include_cinema=False):
	'''get cinema movies'''
	params = {'email': 'metro@cinemahub.com', 'password': '123456'}
	# sending get request and saving the response as response object
	login_url = URL + "login"
	rs = requests.session()
	login_response = rs.post(url = login_url, headers=HEADERS, json=params)

	params_2 = {
	 'genre': genre,
	 'sortby': sortby
	 }
	if include_cinema:
		params_2['cinemaname'] = 'Metro'
	if moviename:
		params_2['moviename'] = moviename
	# sending get request and saving the response as response object
	url = URL + "searchmovie"
	response = rs.post(url = url, headers=HEADERS, json=params_2)
	# extracting data in json format
	data = response.json()
	print('response:\n', data['data'])
	if data['ok']== True and response.status_code == 200:
		print("Passed")
	else:
		print("Failed")
	print()


def search_cinema(sortby, cinemaname=None, include_location=False):
	'''get cinema movies'''
	params = {'email': 'metro@cinemahub.com', 'password': '123456'}
	# sending get request and saving the response as response object
	login_url = URL + "login"
	rs = requests.session()
	login_response = rs.post(url = login_url, headers=HEADERS, json=params)

	params_2 = {
	 'sortby': sortby
	 }
	if cinemaname:
		params_2['name'] = cinemaname
	if include_location:
		params_2['location'] = {'latitude': 90, 'longitude': 70}
	# sending get request and saving the response as response object
	url = URL + "searchcinema"
	response = rs.post(url = url, headers=HEADERS, json=params_2)
	# extracting data in json format
	data = response.json()
	print('response:\n', data['data'])
	if data['ok']== True and response.status_code == 200:
		print("Passed")
	else:
		print("Failed")
	print()


def top_cinemas(k=10):
	'''show top k ranked cinemas'''
	# defining a params dict for the parameters to be sent to the API
	params = {'email': 'admin@cinemahub.com', 'password': '123456'}
	# sending get request and saving the response as response object
	login_url = URL + "login"
	rs = requests.session()
	login_response = rs.post(url = login_url, headers=HEADERS, json=params)

	# pass the k parameter
	params_2 = {'num': k}
	# sending get request and saving the response as response object
	url = URL + "topcinemas"
	response = rs.post(url = url, headers=HEADERS, json=params_2)
	# extracting data in json format
	data = response.json()
	print('response:', data['data'])
	if data['ok']== True and response.status_code == 200:
		print("Passed")
	else:
		print("Failed")
	print()


if __name__ == '__main__':
	# print("Test 1: Get cinema movies")
	# get_movies("Metro")
	# print("Test 2: search movie (sort by)")
	# search_movie('All', 'Latest')
	# search_movie('All', 'Oldest')
	# search_movie('All', 'Alphabetical')
	# print("Test 2: search movie")
	# print("Test 3: search movie (genre)")
	# search_movie('Animation', 'Latest')
	# search_movie('Crime', 'Alphabetical')
	# print("Test 4: search movie (moviename)")
	# search_movie('All', 'Alphabetical', moviename='Les')
	# search_movie('Comedy', 'Alphabetical', moviename='The')
	# print("Test 5: search movie (cinemaname)")
	search_movie('Comedy', 'Alphabetical', include_cinema=True)
	# print("Test 6: search cinema (sort by)")
	# search_cinema('Alphabetical', include_location=False)
	# search_cinema('Rate', include_location=False)
	# print("Test 7: search cinema (location)")
	# search_cinema('Nearest', include_location=True)


	# top_cinemas()
