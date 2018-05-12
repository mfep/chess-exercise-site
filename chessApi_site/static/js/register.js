(function () {

const DEFAULT_CONTENTTYPE = "application/json";
const USERS_PATH = "/api/users/";
const SUBMIT_PAGE = "/site/submitpage.html";

function saveUserToPrefs(nickname, email) {
    window.localStorage.setItem("community-chess-nickname", nickname);
    window.localStorage.setItem("community-chess-email", email);
}

function registerButtonClicked() {
    var nickname = $("#register-nickname").val();
    var email = $("#register-email").val();

    var userUrl = USERS_PATH + nickname + "/";

    $.ajax({
        url: userUrl
    }).done(function () {
        // existing user
        var requestData = {
            nickname: nickname,
            email: email,
            former_email: email
        };
        $.ajax({
            url: userUrl,
            type: "PUT",
            contentType: DEFAULT_CONTENTTYPE,
            data: JSON.stringify(requestData)
        }).done(function () {
            alert("Welcome back, " + nickname + "!");
            saveUserToPrefs(nickname, email);
            window.location.replace(SUBMIT_PAGE);
        }).fail(alertRequestFail);
    }).fail(function () {
        // new user
        var requestData = {
            nickname: nickname,
            email: email
        };
        $.ajax({
            url: USERS_PATH,
            type: "POST",
            contentType: DEFAULT_CONTENTTYPE,
            data: JSON.stringify(requestData)
        }).done(function () {
            alert(nickname + ", welcome on the Chess Community Site");
            saveUserToPrefs(nickname, email);
            window.location.replace(SUBMIT_PAGE);
        }).fail(alertRequestFail);
    });
    return false;
}

$(function () {
    $("form.login").submit(registerButtonClicked);
});

})();