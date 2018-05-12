(function () {

var exercise_protorow = null;

function processExerciseList(data) {
    function deleteExercise(exerciseid, row) {
        var loginInfo = getLoginInfo();
        if (!loginInfo) {
            return;
        }
        $.ajax({
            url: "/api/exercises/" + exerciseid + "/?author_email=" + encodeURIComponent(loginInfo.email),
            type: "DELETE"
        }).done(function () {
            row.remove();
        }).fail(function (jqXHR, textstatus, errorthrown) {
            var response = JSON.parse(jqXHR.responseText);
            alert(errorthrown + " : " + response["@error"]["@message"]);
        });
    }

    data.items.forEach(function (exerciseItem) {
        var row = exercise_protorow.clone().attr("class", "exercise-row").show();
        var exerciseid = exerciseItem["@controls"].self.href.split("/").slice(-2)[0];
        var solverLink = "solvepage.html?exerciseid=" + exerciseid;
        row.find("a").text(exerciseItem.headline).attr("href", solverLink);
        var loginInfo = getLoginInfo();
        if (loginInfo && loginInfo.nickname === exerciseItem.author) {
            row.find(".oi").show().click(function () {
                deleteExercise(exerciseid, row);
            })
        } else {
            row.find(".oi").hide();
        }
        $("#exercise-all").append(row);
    });
}

function listUsers() {
    function listSubmissions(nickname) {
        $(".exercise-row").remove();
        $.ajax({
            url: "/api/users/" + encodeURIComponent(nickname) + "/submissions/",
            dataType: DATATYPE
        }).done(processExerciseList).fail(function (jqXHR, textstatus, errorthrown) {
            var response = JSON.parse(jqXHR.responseText);
            alert(errorthrown + " : " + response["@error"]["@message"]);
        });
    }

    function deleteUser(nickname, row) {
        var loginInfo = getLoginInfo();
        if (!loginInfo || loginInfo.nickname !== nickname) {
            return;
        }
        $.ajax({
            url: "/api/users/" + nickname + "/?email=" + encodeURIComponent(loginInfo.email),
            type: "DELETE"
        }).done(function () {
            row.remove();
        }).fail(function (jqXHR, textstatus, errorthrown) {
            var response = JSON.parse(jqXHR.responseText);
            alert(errorthrown + " : " + response["@error"]["@message"]);
        });
    }

    var user_protorow = $("#user-proto-row").hide();

    $.ajax({
        url: "/api/users/",
        dataType: DATATYPE
    }).done(function (data) {
        data.items.forEach(function (userItem) {
            var row = user_protorow.clone().show();
            row.find("a").text(userItem.nickname).click(function () {
                listSubmissions(userItem.nickname);
            });
            // TODO delete users
            row.find(".oi").hide();
            $("#user-all").append(row);
        });
    }).fail(function (jqXHR, textstatus, errorthrown) {
            var response = JSON.parse(jqXHR.responseText);
            alert(errorthrown + " : " + response["@error"]["@message"]);
    });
}

function listExercises() {
    exercise_protorow = $("#exercise-proto-row").hide();
    $.ajax({
        url: "/api/exercises/",
        dataType: DATATYPE
    }).done(processExerciseList).fail(function (jqXHR, textstatus, errorthrown) {
        var response = JSON.parse(jqXHR.responseText);
        alert(errorthrown + " : " + response["@error"]["@message"]);
    });
}

$(function () {
    listUsers();
    listExercises();
});

})();

