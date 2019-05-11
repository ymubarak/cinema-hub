$(document).ready(function () {

	$('#add_movie_btn').click(function () {
		$("#add_movie_box").show();
		$('#myTable').parents('div.dataTables_wrapper').first().hide();
		// $("#myTable").hide();
	});

	$('#cancel_adding').click(function () {
		$("#add_movie_box").hide();
		// $("#myTable").show();
		$('#myTable').parents('div.dataTables_wrapper').first().show();

	});

	$('#edit_movie_btn').click(function () {
		$("#edit_movie_box").show();
		$('#myTable').parents('div.dataTables_wrapper').first().hide();
		// $("#myTable").hide();
	});

	$('#cancel_editing').click(function () {
		$("#edit_movie_box").hide();
		// $("#myTable").show();
		$('#myTable').parents('div.dataTables_wrapper').first().show();

	});

	$('#edit_movie').click(function () {
		var jsonData = {};
		var formData = $("#edit_cinema_form").serializeArray();
		$.each(formData, function () {
			if (jsonData[this.name]) {
				if (!jsonData[this.name].push) {
					jsonData[this.name] = [jsonData[this.name]];
				}
				jsonData[this.name].push(this.value || '');
			} else {
				jsonData[this.name] = this.value || '';
			}
		});
		// jsonData['genre'] = [jsonData['genre']]
		jsonData['price'] = parseInt(jsonData['price'])
		console.log(jsonData)
		$.ajax(
			{
				type: 'POST',
				contentType: "application/json; charset=utf-8",
				dataType: 'json',
				url: '/editmovie',
				data: JSON.stringify(jsonData),
				success: function (result) {
					if (result['ok'] == true) {
						alert(result['message'])
						window.location.href = "/profile/cinema_profile.html";
					}
				},
				error: function (errormsg) {
					console.log(errormsg);
					alert(errormsg['responseJSON']['message']);
				}
			});
	});

	$('#add_movie').click(function () {
		var jsonData = {};
		var formData = $("#add_cinema_form").serializeArray();
		$.each(formData, function () {
			if (jsonData[this.name]) {
				if (!jsonData[this.name].push) {
					jsonData[this.name] = [jsonData[this.name]];
				}
				jsonData[this.name].push(this.value || '');
			} else {
				jsonData[this.name] = this.value || '';
			}
		});
		// jsonData['genre'] = [jsonData['genre']]
		jsonData['price'] = parseInt(jsonData['price'])
		console.log(jsonData)
		$.ajax(
			{
				type: 'POST',
				contentType: "application/json; charset=utf-8",
				dataType: 'json',
				url: '/addmovie',
				data: JSON.stringify(jsonData),
				success: function (result) {
					if (result['ok'] == true) {
						alert(result['message'])
						window.location.href = "/profile/cinema_profile.html";
					}
				},
				error: function (errormsg) {
					console.log(errormsg);
					alert(errormsg['responseJSON']['message']);
				}
			});
	});
	var movies = []

	function load_movies(data) {
		movies = []
		var i = 0
		var old_tbody = document.getElementById('myTable').getElementsByTagName('tbody')[0];
		var new_tbody = document.createElement('tbody');
		data.forEach(function (element) {
			movies.push(element)
			// Insert a row in the table at the last row
			var newRow = new_tbody.insertRow(i);
			var newCell = newRow.insertCell(0);
			newCell.innerHTML = element['name']

			newCell = newRow.insertCell(1);
			newCell.innerHTML = element['genre']

			newCell = newRow.insertCell(2);
			newCell.innerHTML = element['director']

			newCell = newRow.insertCell(3);
			newCell.innerHTML = element['price']

			newCell = newRow.insertCell(4);
			newCell.innerHTML = element['starting_date']

			newCell = newRow.insertCell(5);
			newCell.innerHTML = '<input type=\"button\" value=\"Edit\" class=\"btn btn-primary btn-xs\">'
				+ '<input style="margin-left: 10px;" type=\"button\" value=\"Delete\" class=\"btn btn-danger btn-xs\">'

			i++
		});
		document.getElementById('myTable').replaceChild(new_tbody, old_tbody)
	}
	$('#myTable').on('click', '.btn-danger', function (e) {
		var movieName = $(this).closest('tr')[0]['childNodes'][0]['innerHTML'];
		$.ajax(
			{
				type: 'DELETE',
				contentType: "application/json; charset=utf-8",
				dataType: 'json',
				url: '/removemovie',
				data: JSON.stringify({ 'movie_name': movieName }),
				success: function (result) {
					if (result['ok'] == true) {
						alert(result['message'])
						window.location.href = "/profile/cinema_profile.html";
					}
				},
				error: function (errormsg) {
					console.log(errormsg);
					alert(errormsg['responseJSON']['message']);
				}
			});
	});


	$('#myTable').on('click', '.btn-primary', function (e) {
		$("#edit_movie_box").show();
		$('#myTable').parents('div.dataTables_wrapper').first().hide();

		var list = $(this).closest('tr')[0]['childNodes']

		$('#edit_movie_box input[name="name"]').val(list[0]['innerHTML']);
		$('#edit_movie_box input[name="genre"]').val(list[1]['innerHTML']);
		$('#edit_movie_box input[name="director"]').val(list[2]['innerHTML']);
		$('#edit_movie_box input[name="price"]').val(list[3]['innerHTML']);
		$('#edit_movie_box input[name="starting_date"]').val(list[4]['innerHTML']);
	});
	function get_profile() {
		$.ajax(
			{
				type: 'GET',
				contentType: "application/json; charset=utf-8",
				dataType: 'json',
				url: '/profile',
				success: function (result) {
					if (result['ok'] == true) {
						var data = result['data']
						$('#cinema_name').text(data['uname'])
						var cover = data['cover'].trim.length == 0 ? '/static/movies/img/cover.jpg' : data['cover'].trim
						$('#cinema_cover').attr("src", cover);
						load_movies(data['movies'])
					}
				},
				error: function (errormsg) {
					console.log(errormsg);
					alert(errormsg['responseJSON']['message']);
				}
			});
	}



	get_profile();

});