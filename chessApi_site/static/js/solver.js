const DEFAULT_DATATYPE = "json";
const EXERCISES_PATH = "/api/exercises/";

const opponentWaitMs = 500;
var chessBoard = null;
var chessGame = null;
var fullMoveList = null;
var movelist = "";
var moveEnabled = true;

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
    if (!moveEnabled) {
        return;
    }
    if (chessGame.move({from: fromsan, to: tosan})) {
        var history = chessGame.history();
        var newSan = history[history.length - 1];
        var testMovelist = movelist === "" ? "" : movelist + ",";
        testMovelist = testMovelist + newSan;
        getSolverResult(testMovelist);
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
        // TODO restrict full move list to server, and return opponent move with solver
        fullMoveList = data["list-moves"].split(",");
        chessBoard.registerBoardClickCallback(boardClickCallback);
        chessGame = new Chess(data["initial-state"]);
        chessBoard.drawPieces(chessGame);
    }).fail(function (jqXHR, textStatus, errorThrown) {
        $("#message").text("Error receiving exercise data: " + errorThrown);
    })
}

function getSolverResult (newMoveList, callback) {
    moveEnabled = false;
    var apiurl = EXERCISES_PATH + getUrlParameter("exerciseid") + "/solver?solution=" + encodeURIComponent(newMoveList);
    $.ajax({
        url: apiurl,
        dataType: DEFAULT_DATATYPE
    }).done(function (data, textStatus) {
        var solverValue = data["value"];
        if (solverValue === "WRONG") {
            chessGame.undo();
            moveEnabled = true;
        } else {
            chessBoard.drawPieces(chessGame);
            movelist = newMoveList;
            if (solverValue === "SOLUTION") {
                alert("Exercise solved!");
            } else if (solverValue === "PARTIAL") {
                setTimeout(function () {
                    fullMoveList.shift();
                    var opponentMove = fullMoveList[0];
                    fullMoveList.shift();
                    movelist = movelist + "," + opponentMove;
                    chessGame.move(opponentMove);
                    chessBoard.drawPieces(chessGame, true);
                    moveEnabled = true;
                }, opponentWaitMs);
            } else {
                console.log("Error: unexpected solver result");
            }
        }
    }).fail(function (jqXHR, textStatus, errorThrown) {
        console.log("Error receiving solver data: " + errorThrown);
        moveEnabled = true;
    });
}

$(function () {
    chessBoard = new ChessBoard();
    chessBoard.drawBoard();
    getExercise(EXERCISES_PATH + getUrlParameter("exerciseid"));
});

