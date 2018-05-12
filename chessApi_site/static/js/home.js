
var exid;

function getUsers() {
    return $.ajax({
        url: "/api/users",
        dataType: "json"
    }).done(function (data) {
        var html = "";
        for (var i = 0; i<data.items.length;i++){
            html+='<tr><td><a class="user_link nav-link" href="/site/homepage.html"></a>';
            html+=data.items[i].nickname;
            html+='<td><span class="oi oi-trash unselectable" title="trash" aria-hidden="true"></span></td></tr>';
        }
        console.log(data);
        $('#user-all').html(html).on('click', 'td', function () {
              var clickedUser = $(this).text().trim();
              $that = $(this);
              $('#user-all').find('td').removeClass('active');
              $that.addClass('active');
//             console.log(clickedUser);
             function getExercise() {
                      return $.ajax({
                      url: "/api/exercises",
                      dataType: "json",
                      contentType: "application/json"
                    }).done(function (data) {
                         var html = "";
                         html+='<h2><a style="color: #116466" href="/site/homepage.html">'+clickedUser+'\'s Exercises</a></h2>';
                         html+='<tr><th></th></tr><tr><th></th></tr><p></p><tr><th></th></tr><tr><th></th></tr>';
                         html+='<tr><th class="nav-link">Exercise Title</th><th>Solved Times</th><th></th></tr>';
                        for (var i = 0; i<data.items.length; i++){
                           if (data.items[i].author === clickedUser){
                                var location = data.items[i]["@controls"]["self"]["href"];
                                var exid = location.split("/").slice(-2)[0];
//                                console.log(location);
                            html+='<tr><td><a class="exercise_link nav-link" href="/site/solvepage.html?exerciseid='+exid+'">';
                            html+=data.items[i].headline;
                            html+='<th>8</th><th><span class="oi oi-trash" title="trash" aria-hidden="true"></span></td></tr>';
                            }
//                            console.log(data.items[i].author);
                     }
                        console.log(data);
                        $('#exercise-all').html(html);
                         }).fail(function (jqXHR, errorThrown) {
                             console.log("Error receiving exercise data: " + errorThrown);
                              var response = JSON.parse(jqXHR.responseText);
                              alert(errorthrown + " : " + response["@error"]["@message"]);
                          })
        }
        getExercise();
        });
    }).fail(function (errorThrown) {
        console.log("Error receiving exercise data: " + errorThrown);
    })
}

getUsers();

function getExercises() {
    return $.ajax({
        url: "/api/exercises",
        dataType: "json"
    }).done(function (data) {
        var html = "";
        html+='<h2><a style="color: #116466" href="/site/homepage.html">All Exercises</a></h2>';
        html+='<tr><th></th></tr><tr><th></th></tr><p></p><tr><th></th></tr><tr><th></th></tr>';
        html+='<tr><th class="nav-link">Exercise Title</th><th>Solved Times</th><th></th></tr>';
        for (var i = 0; i<data.items.length;i++){
            var location = data.items[i]["@controls"]["self"]["href"];
            var exid = location.split("/").slice(-2)[0];
            html+='<tr><td><a class="exercise_link nav-link" href="/site/solvepage.html?exerciseid='+exid+'">';
            html+=data.items[i].headline;
            html+='<th>8</th><th><span class="oi oi-trash" title="trash" aria-hidden="true"></span></td></tr>';


        }
        console.log(data);
        $('#exercise-all').html(html);

    }).fail(function (errorThrown) {
        console.log("Error receiving exercise data: " + errorThrown);
    })
}

getExercises();

//function submitRequest () {
//    return $.ajax({
//        url: "/api/exercises/",
//        contentType: "application/json",
//        data: JSON.stringify(requestBody),
//        type: "GET"
//    }).done(function (data, textstatus, xhr) {
//        var location = xhr.getResponseHeader("Location");
//        var exerciseid = location.split("/").slice(-2)[0];
//      //  window.location.replace("/site/solvepage.html?exerciseid=" + exerciseid);
//    }).fail(function (jqXHR, textstatus, errorthrown) {
//        var response = JSON.parse(jqXHR.responseText);
//        alert(errorthrown + " : " + response["@error"]["@message"]);
//    })
//}