(function () {

const DEFAULT_CONTENTTYPE = "application/json";
const EXERCISES_PATH = "/api/exercises/";
const EXERCISE_PAGE = "/site/solvepage.html?exerciseid=";
const REG_PAGE = "/site/register.html";

var chessBoard = null;
var chessGame = null;
var settingInitialBoard = true;
var nickname = null;
var email = null;

function updateSubmitBtn() {
    if (checkSubmittable()) {
        $("#submit-btn").text("Submit exercise");
    } else {
        $("#submit-btn").text("Input moves until checkmate");
    }
}

function updateUi() {
    chessBoard.drawPieces(chessGame);
    updateMoveList(chessGame);
    updateSubmitBtn();
}

function checkRegistered() {
    nickname = window.localStorage.getItem(NICKNAME_STORAGE_KEY);
    email = window.localStorage.getItem(EMAIL_STORAGE_KEY);
    if (nickname && email) {
        $("#ex-author").text(nickname);
    } else {
        window.location.replace(REG_PAGE);
    }
}

function checkSubmittable() {
    return (chessGame.turn() === "b")
        && chessGame.in_checkmate()
        && $("#ex-title").val();
}

function initialBoardClick(fromsan, tosan) {
    var fromCol = parseInt(fromsan.slice(1));
    var toCol = parseInt(tosan.slice(1));
    if (fromCol > 0) {
        var pickedUp = chessGame.remove(fromsan);
    } else {
        var color = fromCol === 0 ? "w" : "b";
        var figure = ["k", "q", "r", "n", "b", "p"][fromsan.charCodeAt(0) - "a".charCodeAt(0)];
        pickedUp = {color: color, type: figure};
    }
    if (toCol > 0) {
        chessGame.put(pickedUp, tosan);
    }
    chessBoard.drawPieces(chessGame);
}

function setMovesClick(fromsan, tosan) {
    if (chessGame.move({from: fromsan, to: tosan})) {
        updateUi();
    }
}

function submitBtnClicked() {
    if (settingInitialBoard) {
        $("#ex-initial-board").text(chessGame.fen());
        chessBoard.registerBoardClickCallback(setMovesClick);
        settingInitialBoard = false;
        updateUi();
    } else if (checkSubmittable()) {
        submitRequest();
    }
}

function submitRequest() {
    var requestBody = {
        headline: $("#ex-title").val(),
        about: $("#ex-about").val(),
        author: nickname,
        "author-email": email,
        "initial-state": $("#ex-initial-board").text(),
        "list-moves": chessGame.history().join()
    };

    $.ajax({
        url: EXERCISES_PATH,
        contentType: DEFAULT_CONTENTTYPE,
        data: JSON.stringify(requestBody),
        type: "POST"
    }).done(function (data, textstatus, xhr) {
        var location = xhr.getResponseHeader("Location");
        var exerciseid = location.split("/").slice(-2)[0];
        window.location.replace(EXERCISE_PAGE + exerciseid);
    }).fail(function (jqXHR, textstatus, errorthrown) {
        var response = JSON.parse(jqXHR.responseText);
        alert(errorthrown + " : " + response["@error"]["@message"]);
    })
}

$(function () {
    checkRegistered();

    chessGame = new Chess();
    chessBoard = new ChessBoard(true);
    chessBoard.drawBoard();
    chessBoard.registerBoardClickCallback(initialBoardClick);
    chessBoard.drawPieces(chessGame);

    $("#submit-btn").click(submitBtnClicked);
    $("#ex-title").change(function () {
        updateSubmitBtn();
    });
    $("#undo-btn").click(function () {
        chessGame.undo();
        updateUi();
    });
    $("#revert-btn").click(function () {
        if (!settingInitialBoard) {
            chessGame = new Chess($("#ex-initial-board").text());
            updateUi();
        }
    });
    $("#start-over-btn").click(function () {
        chessGame = new Chess();
        settingInitialBoard = true;
        updateUi();
    })
});

})();