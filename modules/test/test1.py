# importing the requests library
import requests

# api-endpoint
URL = "http://0.0.0.0:5000/"
HEADERS = {
    'type': 'POST',
    'contentType': "application/json; charset=utf-8",
    'dataType': 'json',
}

def enter_without_login():
	'''Enter website without login'''
	url = URL
	response = requests.get(url = url)
	print("Redirected to:", response.url)
	if response.url == URL+"register":
		print("Passed")
	else:
		print("Failed")
	print()


def valid_admin_login():
	'''correct admin login'''
	# defining a params dict for the parameters to be sent to the API
	params = {'email': 'murad@cinemahub.com', 'password': '123456'}
	# sending get request and saving the response as response object
	url = URL + "login"
	response = requests.post(url = url, headers=HEADERS, json=params)
	# extracting data in json format
	data = response.json()
	# print(data)
	if data['ok']== True and response.status_code == 200:
		print("Passed")
	else:
		print("Failed")
	print()


def invalid_admin_login():
	'''Non existing admin email '''
	# defining a params dict for the parameters to be sent to the API
	params = {'email': 'invalidadmin@cinemahub.com', 'password': '123456'}
	# sending get request and saving the response as response object
	url = URL + "login"
	response = requests.post(url = url, headers=HEADERS, json=params)
	# extracting data in json format
	data = response.json()
	print("Response:", data['message'])
	if data['ok']== False and response.status_code == 401:
		print("Passed")
	else:
		print("Failed")
	print()


def invalid_admin_login_2():
	'''Incorrect password '''
	# defining a params dict for the parameters to be sent to the API
	params = {'email': 'murad@cinemahub.com', 'password': '1234567'}
	# sending get request and saving the response as response object
	url = URL + "login"
	response = requests.post(url = url, headers=HEADERS, json=params)
	# extracting data in json format
	data = response.json()
	print("Response:", data['message'])
	if data['ok']== False and response.status_code == 401:
		print("Passed")
	else:
		print("Failed")
	print()


def admin_profile():
	'''Valid Admin profile request'''
	# defining a params dict for the parameters to be sent to the API
	params = {'email': 'admin@admin.com', 'password': '123456'}
	# sending get request and saving the response as response object
	login_url = URL + "login"
	rs = requests.session()
	login_response = rs.post(url = login_url, headers=HEADERS, json=params)

	# once logged go to profile
	profile_url = URL + "profile"
	profile_response = rs.get(url = profile_url, headers=HEADERS)

	# extracting data in json format
	data = profile_response.json()
	if data['ok']== True and data['data']['type'] == 'A' and profile_response.status_code == 200:
		print("Passed")
	else:
		print("Failed")
	print()


def valid_cinema_addition():
	'''add new cinema'''
	# defining a params dict for the parameters to be sent to the API
	params = {'uname': 'murad','email': 'murad@cinemahub.com', 'password': '123456'}
	# sending get request and saving the response as response object
	login_url = URL + "login"
	rs = requests.session()
	login_response = rs.post(url = login_url, headers=HEADERS, json=params)

	# once logged add cinema
	params_2 = {'uname': 'Metro', 'email': 'newcinema@cinemahub.com', 'password': '123456'}
	# sending get request and saving the response as response object
	url = URL + "registercinema"
	response = rs.post(url = url, headers=HEADERS, json=params_2)
	# extracting data in json format
	data = response.json()
	print('response:', data['message'])
	if data['ok']== True and response.status_code == 200:
		print("Passed")
	else:
		print("Failed")
	print()


def invalid_cinema_addition():
	'''add already existing email'''
	# defining a params dict for the parameters to be sent to the API
	params = {'uname': 'murad', 'email': 'murad@cinemahub.com', 'password': '123456'}
	# sending get request and saving the response as response object
	login_url = URL + "login"
	rs = requests.session()
	login_response = rs.post(url = login_url, headers=HEADERS, json=params)

	# once logged add cinema
	params_2 = {'uname': 'Metro', 'email': 'newcinema@cinemahub.com', 'password': '123456'}
	# sending get request and saving the response as response object
	url = URL + "registercinema"
	response = rs.post(url = url, headers=HEADERS, json=params_2)
	# extracting data in json format
	data = response.json()
	print('response:', data['message'])
	if data['ok']== False and response.status_code == 400:
		print("Passed")
	else:
		print("Failed")
	print()

def invalid_cinema_addition_2():
	'''add already existing cinema name'''
	# defining a params dict for the parameters to be sent to the API
	params = {'uname': 'murad', 'email': 'murad@cinemahub.com', 'password': '123456'}
	# sending get request and saving the response as response object
	login_url = URL + "login"
	rs = requests.session()
	login_response = rs.post(url = login_url, headers=HEADERS, json=params)

	# once logged add cinema
	params_2 = {'uname': 'Metro', 'email': 'mycinema@cinemahub.com', 'password': '123456'}
	# sending get request and saving the response as response object
	url = URL + "registercinema"
	response = rs.post(url = url, headers=HEADERS, json=params_2)
	# extracting data in json format
	data = response.json()
	print('response:', data['message'])
	if data['ok']== False and response.status_code == 400:
		print("Passed")
	else:
		print("Failed")
	print()

def invalid_cinema_addition_3():
	'''bad email format'''
	# defining a params dict for the parameters to be sent to the API
	params = {'uname': 'murad', 'email': 'murad@cinemahub.com', 'password': '123456'}
	# sending get request and saving the response as response object
	login_url = URL + "login"
	rs = requests.session()
	login_response = rs.post(url = login_url, headers=HEADERS, json=params)

	# once logged add cinema
	params_2 = {'uname': 'Metro', 'email': 'mycinema@gmail.com', 'password': '123456'}
	# sending get request and saving the response as response object
	url = URL + "registercinema"
	response = rs.post(url = url, headers=HEADERS, json=params_2)
	# extracting data in json format
	data = response.json()
	print('response:', data['message'])
	if data['ok']== False and response.status_code == 400:
		print("Passed")
	else:
		print("Failed")
	print()

def delete_cinema():
	'''delete existing cinema'''
	# defining a params dict for the parameters to be sent to the API
	params = {'email': 'murad@cinemahub.com', 'password': '123456'}
	# sending get request and saving the response as response object
	login_url = URL + "login"
	rs = requests.session()
	login_response = rs.post(url = login_url, headers=HEADERS, json=params)

	# once logged delete cinema
	params_2 = {'email': 'newcinema@cinemahub.com'}
	# sending get request and saving the response as response object
	url = URL + "unregistercinema"
	response = rs.post(url = url, headers=HEADERS, json=params_2)
	# extracting data in json format
	data = response.json()
	print('response:', data['message'])
	if data['ok']== True and response.status_code == 200:
		print("Passed")
	else:
		print("Failed")
	print()


def invalid_delete_cinema():
	'''delete non-existing cinema'''
	# defining a params dict for the parameters to be sent to the API
	params = {'email': 'murad@cinemahub.com', 'password': '123456'}
	# sending get request and saving the response as response object
	login_url = URL + "login"
	rs = requests.session()
	login_response = rs.post(url = login_url, headers=HEADERS, json=params)

	# once logged go to profile
	params_2 = {'name': 'Metro', 'email': 'non-existing@cinemahub.com', 'password': '123456'}
	# sending get request and saving the response as response object
	url = URL + "unregistercinema"
	response = rs.post(url = url, headers=HEADERS, json=params_2)
	# extracting data in json format
	data = response.json()
	print('response:', data['message'])
	if data['ok']== False and response.status_code == 400:
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


def logout():
	url = URL + "logout"
	response = requests.get(url = url)
	print("Redirected to:", response.url)
	if response.url == URL+"register":
		print("Passed")
	else:
		print("Failed")
	print()


if __name__ == '__main__':
	print("Test 0: Enter website without login")
	enter_without_login()
	print("Test 1: correct admin login")
	valid_admin_login()
	print("Test 2: Non existing email")
	invalid_admin_login()
	print("Test 3: Incorrect password")
	invalid_admin_login_2()
	print("Test 4: Valid Admin profile request")
	admin_profile()
	print("Test 5: logout")
	logout()
	print("Test 6: add new cinema")
	valid_cinema_addition()
	print("Test 7: add cinema with already existing email")
	invalid_cinema_addition()
	print("Test 8: add already existing cinema name")
	invalid_cinema_addition_2()
	print("Test 9: add cinema with bad email format")
	invalid_cinema_addition_3()
	print("Test 10: delete existing cinema")
	delete_cinema()
	print("Test 11: delete non-existing cinema")
	invalid_delete_cinema()
	print("Test 12: show top k ranked cinemas")
	top_cinemas(k=10)
