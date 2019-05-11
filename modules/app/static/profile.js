$(document).ready(function () {
    $("#show_addbox").click(function () {
        $("#addbox").show();
        $('#deletebox').hide();
        $('#rankbox').hide();
        $('#cinema_box').hide();
    });

    $("#show_deletebox").click(function () {
        $("#addbox").hide();
        $('#deletebox').show();
        $('#rankbox').hide();
        $('#cinema_box').hide();
    });

    $("#show_rankbox").click(function () {
        $("#addbox").hide();
        $('#deletebox').hide();
        $('#rankbox').show();
        $('#cinema_box').hide();
        var jsonData = {};
        jsonData['num'] = cinemas.length;
        $.ajax(
            {
                type: 'POST',
                contentType: "application/json; charset=utf-8",
                dataType: 'json',
                url: '/topcinemas',
                data: JSON.stringify(jsonData),
                success: function (result) {
                    if (result['ok'] == true) {
                        show_rank(result['data'])
                    }
                },
                error: function (errormsg) {
                    console.log(errormsg);
                    alert(errormsg['responseJSON']['message']);
                }
            });
    });

    function show_rank(data) {
        var old_tbody = document.getElementById('rank_table').getElementsByTagName('tbody')[0];
        var new_tbody = document.createElement('tbody');
        for (var i = 0; i < data.length; i++) {
            // Insert a row in the table at the last row
            var newRow = new_tbody.insertRow(i);
            var newCell = newRow.insertCell(0);
            newCell.innerHTML = (i + 1)
            newCell = newRow.insertCell(1);
            newCell.innerHTML = data[i]['name']

            newCell = newRow.insertCell(2);
            var rate = data[i]['rate']
            newCell.innerHTML = '<span class=\"label ' + get_label(rate) + '\">' + rate + '</span>'
        }
        document.getElementById('rank_table').replaceChild(new_tbody, old_tbody)
    }

    function get_label(rate) {
        if (rate <= 1) {
            return 'label-default'
        } else if (rate > 1 && rate <= 2) {
            return 'label-primary'
        } else if (rate > 2 && rate <= 3) {
            return 'label-success'
        } else if (rate > 3 && rate <= 4) {
            return 'label-warning'
        } else {
            return 'label-danger'
        }
    }

    function search_cinema(data) {
        $.ajax(
            {
                type: 'POST',
                contentType: "application/json; charset=utf-8",
                dataType: 'json',
                url: '/searchcinema',
                data: JSON.stringify(data),
                success: function (result) {
                    if (result['ok'] == true) {
                        console.log(result['data'])
                        load_cinemas(result['data']);
                    }
                },
                error: function (errormsg) {
                    console.log(errormsg);
                }
            });
    }
    $("#search_cinema").click(function (e) {
        var data = {};
        data['name'] = $("#search_cinema_name").val();
        data['sortby'] = 'Alphabetical';
        search_cinema(data);
        e.preventDefault();
    });

    $('#delete_cinema_btn').click(function (e) {
        var jsonData = {};
        jsonData['email'] = $("#deleted_cinema_email").val();
        $.ajax(
            {
                type: 'POST',
                contentType: "application/json; charset=utf-8",
                dataType: 'json',
                url: '/unregistercinema',
                data: JSON.stringify(jsonData),
                success: function (result) {
                    console.log(result)
                    if (result['ok'] == true) {
                        alert(result['message']);
                        window.location.href = "/profile/admin_profile.html";
                    }
                },
                error: function (errormsg) {
                    console.log(errormsg);
                    alert(errormsg['responseJSON']['message']);
                }
            });
    });
    $("#add_cinema").click(function (e) {
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
        console.log(jsonData);
        $.ajax(
            {
                type: 'POST',
                contentType: "application/json; charset=utf-8",
                dataType: 'json',
                url: '/registercinema',
                data: JSON.stringify(jsonData),
                success: function (result) {
                    console.log(result)
                    if (result['ok'] == true) {
                        alert(result['message']);
                        window.location.href = "/profile/admin_profile.html";
                    }
                },
                error: function (errormsg) {
                    console.log(errormsg);
                    alert(errormsg['responseJSON']['message']);
                }
            });
        e.preventDefault();
    });


    var cinemas = []

    function get_all_cinemas() {
        var data = {};
        data['sortby'] = 'Alphabetical';
        search_cinema(data);
    }

    function load_cinemas(data) {
        cinemas = []
        var text = ''
        data.forEach(function (element) {
            cinemas.push(element)
            // var email = element['name']
            var name =  element['name'] //email.substring(0, email.indexOf('@'))
            var cover = element['cover'].trim.length == 0 ? '/static/movies/img/cover.jpg' : element['cover'].trim
            text += '<div class=\"col-xs-10 col-sm-4\">'
            text += '<figure><img src=\" ' + cover + '\" width=\"200\" height=\"255\"</figure>'
            text += '<br><div><a href=\"#\">' + name + '</a>'
            text += '</div></div>'
        });
        var node = document.getElementById('cinema_box_row');
        node.innerHTML = text
    }

    get_all_cinemas();
});

/**
 * <tr>
                                        <td>1</td>
                                        <td>Metro</td>
                                        <td>
                                            <span class="label label-success">4.3</span>
                                        </td>
                                    </tr>
 */