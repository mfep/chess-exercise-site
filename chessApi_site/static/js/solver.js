const DEFAULT_DATATYPE = "json";
const EXERCISES_PATH = "/api/exercises/";

var chessBoard = null;
var chessGame = null;

// from stackoverflow
function getUrlParameter(sParam) {
    var sPageURL = decodeURIComponent(window.location.search.substring(1)),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;
    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');
        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : sParameterName[1];
        }
    }
}

function boardClickCallback (fromsan, tosan) {
    if (chessGame.move({from: fromsan, to: tosan})) {
        chessBoard.drawPieces(chessGame);
    }
}

function getExercise(apiurl) {
    return $.ajax({
        url: apiurl,
        dataType: DEFAULT_DATATYPE
    }).done(function (data, textStatus) {
        $("#message").text("Exercise data retrieved");
        $("#ex-title").text(data.headline);
        $("#ex-about").text(data.about);
        $("#ex-author").text(data.author);

        chessBoard.registerBoardClickCallback(boardClickCallback);
        chessGame = new Chess(data["initial-state"]);
        chessBoard.drawPieces(chessGame);
    }).fail(function (jqXHR, textStatus, errorThrown) {
        $("#message").text("Error receiving exercise data: " + errorThrown);
    })
}

$(function () {
    chessBoard = new ChessBoard();
    chessBoard.drawBoard();
    getExercise(EXERCISES_PATH + getUrlParameter("exerciseid"));
});

