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