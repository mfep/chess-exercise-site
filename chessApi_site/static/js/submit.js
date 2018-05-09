var chessBoard = null;
var chessGame = null;

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

$(function () {
    chessGame = new Chess();
    chessBoard = new ChessBoard(true);
    chessBoard.drawBoard();
    chessBoard.registerBoardClickCallback(initialBoardClick);
    chessBoard.drawPieces(chessGame);
});