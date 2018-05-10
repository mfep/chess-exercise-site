const DEFAULT_DATATYPE = "json";
const DEFAULT_CONTENTTYPE = "application/json";
const EXERCISES_PATH = "/api/exercises/";

var chessBoard = null;
var chessGame = null;
var initialBoardSet = true;

function checkSubmittable () {
    return (chessGame.turn() === "b") && chessGame.in_checkmate();
}

function initialBoardClick (fromsan, tosan) {
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

function setMovesClick (fromsan, tosan) {
    if (chessGame.move({from: fromsan, to:tosan})) {
        chessBoard.drawPieces(chessGame);
        if (checkSubmittable()) {
            $("#submit-btn").text("Submit exercise");
        } else {
            $("#submit-btn").text("Input moves until checkmate");
        }
    }
}

function submitBtnClicked () {
    if (initialBoardSet) {
        $("#ex-initial-board").text(chessGame.fen());
        chessBoard.registerBoardClickCallback(setMovesClick);
        $("#submit-btn").text("Input moves until checkmate");
        initialBoardSet = false;
    } else if (checkSubmittable()) {
        submitRequest();
    }
}

function submitRequest () {
    const author = "Mystery";
    const authormail = "mystery@mymail.com";

    var requestBody = {
        headline: $("#ex-title").text(),
        about: $("#ex-about").text(),
        author: author,
        "author-email": authormail,
        "initial-state": $("#ex-initial-board").text(),
        "list-moves": chessGame.history().join()
    };

    $.ajax({
        url: EXERCISES_PATH,
        contentType: DEFAULT_CONTENTTYPE,
        data: JSON.stringify(requestBody),
        type: "POST"
    }).done(function (data, textstatus) {
        console.log(data, textstatus);
    }).fail(function (jqXHR, textstatus, errorthrown) {
        console.log(jqXHR.responseText, textstatus, errorthrown);
    })
}

$(function () {
    chessGame = new Chess();
    chessBoard = new ChessBoard(true);
    chessBoard.drawBoard();
    chessBoard.registerBoardClickCallback(initialBoardClick);
    chessBoard.drawPieces(chessGame);

    $("#submit-btn").click(submitBtnClicked);
});