# importing the requests library
import requests

# api-endpoint
URL = "http://0.0.0.0:5000/"
HEADERS = {
    'type': 'POST',
    'contentType': "application/json; charset=utf-8",
    'dataType': 'json',
}

def valid_cinema_login():
	'''add new cinema'''
	# defining a params dict for the parameters to be sent to the API
	params = {'email': 'testcinema@cinemahub.com', 'password': '123456'}
	# sending get request and saving the response as response object
	login_url = URL + "login"
	rs = requests.session()
	response = rs.post(url = login_url, headers=HEADERS, json=params)

	# extracting data in json format
	data = response.json()
	if data['ok']== True and response.status_code == 200:
		print("Passed")
	else:
		print("Failed")
	print()


def valid_movie_addition():
	'''add new movie'''
	# defining a params dict for the parameters to be sent to the API
	params = {'email': 'testcinema@cinemahub.com', 'password': '123456'}
	# sending get request and saving the response as response object
	login_url = URL + "login"
	rs = requests.session()
	login_response = rs.post(url = login_url, headers=HEADERS, json=params)

	# once logged add movie
	params_2 = {
	 'name': 'Venom',
	 'genre': 'Thriller',
	 'director': 'Ruben Fleischer',
	 'price': 35.0,
	 'starting_date': '2012-04-15',
	 }
	# sending get request and saving the response as response object
	url = URL + "addmovie"
	response = rs.post(url = url, headers=HEADERS, json=params_2)
	# extracting data in json format
	data = response.json()
	print('response:', data['message'])
	if data['ok']== True and response.status_code == 200:
		print("Passed")
	else:
		print("Failed")
	print()


def invalid_movie_addition():
	'''add existing movie'''
	# defining a params dict for the parameters to be sent to the API
	params = {'email': 'testcinema@cinemahub.com', 'password': '123456'}
	# sending get request and saving the response as response object
	login_url = URL + "login"
	rs = requests.session()
	login_response = rs.post(url = login_url, headers=HEADERS, json=params)

	# once logged add movie
	params_2 = {
	 'name': 'Venom',
	 'genre': 'Thriller',
	 'director': 'Ruben Fleischer',
	 'price': 35.0,
	 'starting_date': '2012-04-15',
	 }
	# sending get request and saving the response as response object
	url = URL + "addmovie"
	response = rs.post(url = url, headers=HEADERS, json=params_2)
	# extracting data in json format
	data = response.json()
	print('response:', data['message'])
	if data['ok']== False and response.status_code == 400:
		print("Passed")
	else:
		print("Failed")
	print()

def get_movies():
	'''get cinema movies'''
	# defining a params dict for the parameters to be sent to the API
	params = {'email': 'murad@cinemahub.com', 'password': '123456'}
	# sending get request and saving the response as response object
	login_url = URL + "login"
	rs = requests.session()
	login_response = rs.post(url = login_url, headers=HEADERS, json=params)

	# once logged add movie
	params_2 = {
	 'cinema_name': 'Amir',
	 }
	# sending get request and saving the response as response object
	url = URL + "getmovies"
	response = rs.post(url = url, headers=HEADERS, json=params_2)
	# extracting data in json format
	data = response.json()
	print('response:\n', data['data'])
	if data['ok']== True and response.status_code == 200:
		print("Passed")
	else:
		print("Failed")
	print()


def valid_movie_removal():
	'''delete existing movie'''
	# defining a params dict for the parameters to be sent to the API
	params = {'email': 'testcinema@cinemahub.com', 'password': '123456'}
	# sending get request and saving the response as response object
	login_url = URL + "login"
	rs = requests.session()
	login_response = rs.post(url = login_url, headers=HEADERS, json=params)

	# once logged add movie
	params_2 = {
	 'movie_name': 'Venom',
	 }
	# sending get request and saving the response as response object
	url = URL + "removemovie"
	response = rs.delete(url = url, headers=HEADERS, json=params_2)
	# extracting data in json format
	data = response.json()
	print('response:', data['message'])
	if data['ok']== True and response.status_code == 200:
		print("Passed")
	else:
		print("Failed")
	print()


def invalid_movie_removal():
	'''delete non-existing movie'''
	# defining a params dict for the parameters to be sent to the API
	params = {'email': 'testcinema@cinemahub.com', 'password': '123456'}
	# sending get request and saving the response as response object
	login_url = URL + "login"
	rs = requests.session()
	login_response = rs.post(url = login_url, headers=HEADERS, json=params)

	# once logged add movie
	params_2 = {
	 'movie_name': '12 Angry men',
	 }
	# sending get request and saving the response as response object
	url = URL + "removemovie"
	response = rs.delete(url = url, headers=HEADERS, json=params_2)
	# extracting data in json format
	data = response.json()
	print('response:', data['message'])
	if data['ok']== False and response.status_code == 400:
		print("Passed")
	else:
		print("Failed")
	print()

def valid_cinema_review():
	'''delete non-existing movie'''
	# defining a params dict for the parameters to be sent to the API
	params = {'email': 'murad@cinemahub.com', 'password': '123456'}
	# sending get request and saving the response as response object
	login_url = URL + "login"
	rs = requests.session()
	login_response = rs.post(url = login_url, headers=HEADERS, json=params)

	# once logged add movie
	params_2 = {
	 'cinema_name': 'Amir',
	 'rate': '2'
	 }
	# sending get request and saving the response as response object
	url = URL + "ratecinema"
	response = rs.post(url = url, headers=HEADERS, json=params_2)
	# extracting data in json format
	data = response.json()
	print('response:', data['message'])
	if data['ok']== True and response.status_code == 200:
		print("Passed")
	else:
		print("Failed")
	print()


def top_cinemas(k=10):
	'''show top k ranked cinemas'''
	# defining a params dict for the parameters to be sent to the API
	params = {'email': 'murad@cinemahub.com', 'password': '123456'}
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
	print("Test 1: Valid cinema login")
	valid_cinema_login()
	print("Test 2: Add new movie")
	valid_movie_addition()
	print("Test 3: Add existing movie")
	invalid_movie_addition()
	print("Test 4: Get cinema movies")
	get_movies()
	print("Test 5: delete existing movie")
	valid_movie_removal()
	print("Test 6: delete non-existing movie")
	invalid_movie_removal()
	print("Test 7: Review cinema")
	valid_cinema_review()
	top_cinemas()
