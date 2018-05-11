const NICKNAME_STORAGE_KEY = "community-chess-nickname";
const EMAIL_STORAGE_KEY = "community-chess-email";

function updateMoveList(chessGame) {
    var moveUl = $("#ex-moves");
    moveUl.empty();
    var moves = chessGame.history();
    for (var i = 0; i < moves.length; i+= 2) {
        var str = "";
        str += moves[i];
        if (i+1 < moves.length) {
            str += ", " + moves[i+1]
        }
        moveUl.append("<li>"+ str +"</li>");
    }
}

function updateUserHeader() {
    var nickname = window.localStorage.getItem(NICKNAME_STORAGE_KEY);
    var email = window.localStorage.getItem(EMAIL_STORAGE_KEY);
    if (nickname && email) {
        $("#user-indicator").show();
        $("#user-nickname").text(nickname);
        $("#to-register-btn").hide();
    } else {
        $("#user-indicator").hide();
        $("#to-register-btn").show();
    }
}

$(function () {
    updateUserHeader();
    $("#user-logout").click(function () {
        window.localStorage.removeItem(NICKNAME_STORAGE_KEY);
        window.localStorage.removeItem(EMAIL_STORAGE_KEY);
        updateUserHeader();
    });
});
