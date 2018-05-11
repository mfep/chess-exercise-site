function getUsers() {
    return $.ajax({
        url: "/api/users",
        dataType: "json"
    }).done(function (data) {
        var html = "";
        for (var i = 0; i<data.items.length;i++){
            html+='<tr><th><a class="user_link nav-link " href="/site/homepage.html"></a> ';
//            user'+data.items[i].nickname.toLowerCase()+'.html">';
            html+=data.items[i].nickname;
//
            html+='</a></th><th></th><th<span class="oi oi-trash" title="trash" aria-hidden="true"></span></th></tr>';
        }
        console.log(data);
        $('#user-all').html(html).on('click', 'tr', function () {
            // Show current `tr` and hide others
            $(this).show().siblings().hide();
            var clickedCell = $(this).text().trim();
           //            B(clickedCell);
            console.log(clickedCell);

             function getExercise() {
                      return $.ajax({
                      url: "/api/exercises",
                      dataType: "json"
                    }).done(function (data) {
                      var html = "";
                     html+='<tr><th class="nav-link">Exercise Title</th><th>Solved Times</th><th></th></tr>';
                     for (var i = 0; i<data.items.length;i++){
                           if (data.items[i].author === clickedCell){
                            while(data.items[i].exercise_link){}
                         html+='<tr><th><a class="exercise_link nav-link" href="/site/solvepage.html?exerciseid='+ data.items[i].exerciseid +'">';
                       html+=data.items[i].headline;
                           html+='<th>8</th><th><span class="oi oi-trash" title="trash" aria-hidden="true"></span></th></tr>';
                            }

                            console.log(data.items[i].about);
                     }
                        console.log(data);
                        $('#exercise-all').html(html);
                         }).fail(function (errorThrown) {
                             console.log("Error receiving exercise data: " + errorThrown);
                              })

        }
        getExercise();
        });

    }).fail(function (errorThrown) {
        console.log("Error receiving exercise data: " + errorThrown);
    })
}
// $('.nohidden').show();
getUsers();

function getExercises() {
    return $.ajax({
        url: "/api/exercises",
        dataType: "json"
    }).done(function (data) {
        var html = "";
        html+='<tr><th class="nav-link">Exercise Title</th><th>Solved Times</th><th></th></tr>';
        for (var i = 0; i<data.items.length;i++){

            html+='<tr><th><a class="exercise_link nav-link" href="/site/solvepage.html?exerciseid='+data.items[i].exerciseid+'">';
            html+=data.items[i].headline;
            html+='<th>8</th><th><span class="oi oi-trash" title="trash" aria-hidden="true"></span></th></tr>';


        }
        console.log(data);
        $('#exercise-all').html(html);

    }).fail(function (errorThrown) {
        console.log("Error receiving exercise data: " + errorThrown);
    })
}

getExercises();