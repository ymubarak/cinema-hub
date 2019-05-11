$(document).ready(function () {
    // Handle register
    $("#profile").click(function (e) {
        $.ajax(
            {
                type: 'GET',
                contentType: "application/json; charset=utf-8",
                dataType: 'json',
                url: '/profile',
                success: function (result) {
                    if (result['ok'] == true) {
                        var user = result['data'];
                        if (user['type'] == 'A') {
                            console.log("reditecte");
                            window.location.href = "./profile/admin_profile.html";
                        } else if (user['type'] == 'R') {
                            window.location.href = "./profile/user_profile.html";
                        } else {
                            window.location.href = "./profile/cinema_profile.html";
                        }
                    }
                },
                error: function (errormsg) {
                    console.log(errormsg);
                }
            });
        e.preventDefault();
    });

    $('#serch_cinemas').click(function(e){
        var jsonData = {};
        var formData = $("#search_cinema_form").serializeArray();
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
        get_cinemas(jsonData['name'],jsonData['sortby'])
        e.preventDefault();
    });

    $('#serch_movies').click(function(e){
        var jsonData = {};
        var formData = $("#search_movies_form").serializeArray();
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
        get_movies(jsonData['genre'],jsonData['sortby'],jsonData['moviename'],jsonData['cinemaname'])
        e.preventDefault();
    });

    function load_movies(data) {
        var text = ''
        data.forEach(function (element) {
            text += '<div class="col-md-4 col-sm-6 portfolio-item">'
            text += '<a class="portfolio-link" data-toggle="modal" href="#">'
            text += '<img class="img-fluid" src="'
            cover = element['poster']
            if (!cover)
                cover = 'https://upload.wikimedia.org/wikipedia/en/0/0d/Avengers_Endgame_poster.jpg'
            text += cover + '"></a>'
            text += '<div class="portfolio-caption"><h4>' + element['name'] + '</h4>'
            text += '<p class="text-muted">Genre are ' + element['genre'].toString() + '</p>'
            text += '<p class="text-muted">Price = ' + element['price'] + '$</p>'
            text += '<p class="text-muted">Director is ' + element['director'] + '</p>'
            text += '<p class="text-muted">Starting date ' + element['starting_date'] + '</p>'
            text += '</div></div>'
        });
        var node = document.getElementById('movies_box_row');
        node.innerHTML = text
    }

    function get_movies(genre, sortby, moviename, cinemaname) {
        var parm = {}
        parm['genre'] = genre || 'All'
        parm['sortby'] = sortby || 'Alphabetical'
        if (moviename) parm['moviename'] = moviename
        if (cinemaname) parm['cinemaname'] = cinemaname
        $.ajax(
            {
                type: 'POST',
                contentType: "application/json; charset=utf-8",
                dataType: 'json',
                url: '/searchmovie',
                data: JSON.stringify(parm),
                success: function (result) {
                    if (result['ok'] == true) {
                        console.log(result['data'])
                        load_movies(result['data'])
                    }
                },
                error: function (errormsg) {
                    console.log(errormsg);
                }
            });
    }


    function load_cinemas(data) {
        var text = ''
        data.forEach(function (element) {
            text += '<div class="col-md-4 col-sm-6 portfolio-item">'
            text += '<a class="portfolio-link" data-toggle="modal" href="#">'
            text += '<img class="img-fluid" src="'
            cover = element['cover']
            if (!cover) {
                cover = 'https://freedesignfile.com/upload/2015/06/Film-with-popcorn-cinema-poster-vector-02.jpg'
            }
            text += cover + '"></a>'
            text += '<div class="portfolio-caption"><h4>' + element['name'] + '</h4>'
            text += '<p class="text-muted">Location ' + element['location'] + '</p>'
            text += '</div></div>'
        });
        var node = document.getElementById('cinemas_box_row');
        node.innerHTML = text
    }

    function get_cinemas(name, sortby) {
        var parm = {}
        parm['sortby'] = sortby || 'Alphabetical'
        if (name) parm['name'] = name
        $.ajax(
            {
                type: 'POST',
                contentType: "application/json; charset=utf-8",
                dataType: 'json',
                url: '/searchcinema',
                data: JSON.stringify(parm),
                success: function (result) {
                    if (result['ok'] == true) {
                        console.log(result['data'])
                        load_cinemas(result['data'])
                    }
                },
                error: function (errormsg) {
                    alert(errormsg);
                }
            });
    }

    get_movies(null, null, null, null);
    get_cinemas(null, null);
});