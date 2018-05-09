var ChessBoard = function(showControls) {
    const xmlns = "http://www.w3.org/2000/svg";
    const TILE = 50;
    const PIECE_SCALE = 1.1;

    var tiles = [];
    var pieces = [];
    var svgnode = document.getElementById("chess-board");
    var fromSan = null;
    var highlighter = null;
    var moveHighlighters = [];
    var boardClickCallback = function(fromsan, tosan) { console.log(fromsan, tosan) };

    function createRectGroupClicked (x, y) {
        return function (mouseEv) {
            var target = mouseEv.target;
            while (target.getAttribute("class") !== "rectGroup") {
                target = target.parentElement;
            }
            var san = String.fromCharCode(97 + x) + (8 - y).toString();
            if (fromSan) {
                highlighter.setAttributeNS(null, "visibility", "hidden");
                boardClickCallback(fromSan, san);
                fromSan = null;
            } else {
                highlighter.setAttributeNS(null, "visibility", "visible");
                tiles[y][x].appendChild(highlighter);
                fromSan = san;
            }
        }
    }

    function addPiece(row, col, piece) {
        var pieceElem = document.getElementById(piece).cloneNode(true);
        pieceElem.removeAttribute("id");
        pieceElem.setAttributeNS(null, "transform", "scale(" + PIECE_SCALE + ")");
        tiles[row][col].appendChild(pieceElem);
        return pieceElem;
    }

    function charToChessPieceName(char) {
        var color = char === char.toUpperCase() ? "white" : "black";
        var figure = null;
        switch (char.toLowerCase()) {
            case "r": figure = "rook"; break;
            case "n": figure = "knight"; break;
            case "b": figure = "bishop"; break;
            case "q": figure = "queen"; break;
            case "k": figure = "king"; break;
            case "p": figure = "pawn"; break;
        }
        if (figure) {
            return color+"-"+figure;
        }
        return null;
    }

    this.drawBoard = function () {
        var heightInTiles = showControls ? 11 : 9;
        svgnode.setAttributeNS(null, "width", (9 * TILE).toString());
        svgnode.setAttributeNS(null, "height", (heightInTiles * TILE).toString());

        function addRect(x, y, w, h, color) {
            var groupElem = document.createElementNS(xmlns, "g");
            groupElem.setAttribute("class", "rectGroup");
            var rectElem = document.createElementNS(xmlns, "rect");
            groupElem.setAttributeNS(null, "transform", "translate(" + x + "," + y + ")");
            rectElem.setAttributeNS(null, "width", w);
            rectElem.setAttributeNS(null, "height", h);
            rectElem.setAttributeNS(null, "fill", color);
            groupElem.appendChild(rectElem);
            svgnode.appendChild(groupElem);
            return groupElem;
        }

        function addTextRect(x, y, text) {
            var textElem = document.createElementNS(xmlns, "text");
            textElem.setAttributeNS(null, "x", x);
            textElem.setAttributeNS(null, "y", y);
            textElem.setAttributeNS(null, "text-anchor", "middle");
            var textNode = document.createTextNode(text);
            textElem.appendChild(textNode);
            svgnode.appendChild(textElem);
        }

        function createHighlighter(color) {
            var elem = document.createElementNS(xmlns, "circle");
            elem.setAttributeNS(null, "cx", (TILE/2).toString());
            elem.setAttributeNS(null, "cy", (TILE/2).toString());
            elem.setAttributeNS(null, "r", (TILE/2).toString());
            elem.setAttributeNS(null, "fill", color);
            elem.setAttributeNS(null, "visibility", "hidden");
            tiles[0][0].appendChild(elem);
            return elem;
        }

        // tiles
        for (var y = 0; y < 8; y++) {
            var row = [];
            for (var x = 0; x < 8; x++) {
                var color = (9 * y + x) % 2 ? "#af6336" : "#fcfa9f";
                var rectGroup = addRect(x * TILE + TILE, y * TILE + TILE, TILE, TILE, color);
                rectGroup.onclick = createRectGroupClicked(x, y);
                row.push(rectGroup);
            }
            tiles.push(row);
        }

        // indicator letters
        for (x = 0; x < 8; x++) {
            var letter = String.fromCharCode('a'.charCodeAt(0) + x);
            addTextRect((x+1.5) * TILE, TILE / 2, letter);
        }

        // indicator indices
        for (y = 0; y < 8; y++) {
            addTextRect(TILE / 2, (y+1.5)*TILE, (8-y).toString());
        }

        // highlighter
        highlighter = createHighlighter("#85ff3060");
        moveHighlighters.push(createHighlighter("#f47d4260"));
        moveHighlighters.push(createHighlighter("#f47d4260"));

        // controls
        if (showControls) {
            var figures = ["king", "queen", "rook", "knight", "bishop", "pawn"];
            for (var i = 0; i < 2; i++) {
                row = [];
                for (var col = 0; col < figures.length; col++) {
                    var tile = addRect((col+1) * TILE, (9 + i) * TILE, TILE, TILE, "#e2e2e2");
                    tile.onclick = createRectGroupClicked(col, 8+i);
                    row.push(tile);
                }
                tiles.push(row);
                for (col = 0; col < figures.length; col++) {
                    var figureName = (i ? "black-" : "white-") + figures[col];
                    addPiece(8+i, col, figureName);
                }
            }
        }
    };

    this.drawPieces = function (chessGame, displayLastMove) {
        function placeMoveHighlighter(index, san) {
            var moveHighlighter = moveHighlighters[index];
            var sanLetter = san[0];
            var sanNumber = san[1];
            var row = 8 - sanNumber;
            var col = sanLetter.charCodeAt(0) - "a".charCodeAt(0);

            moveHighlighter.setAttributeNS(null, "visibility", "visible");
            tiles[row][col].appendChild(moveHighlighter);
        }

        this.clearPieces();
        // TODO use chessGame.board instead
        var boardAscii = chessGame.ascii();
        boardAscii = boardAscii.replace(/ /g, '');
        var lines = boardAscii.split("\n");
        for (var y = 0; y < 8; ++y) {
            for (var x = 0; x < 8; ++x) {
                var char = lines[y+1].charAt(x+2);
                var figure = charToChessPieceName(char);
                if (figure) {
                    pieces.push(addPiece(y, x, figure));
                }
            }
        }
        if (displayLastMove) {
            var history = chessGame.history({verbose: true});
            var lastMove = history.slice(-1)[0];
            placeMoveHighlighter(0, lastMove.from);
            placeMoveHighlighter(1, lastMove.to);
        } else {
            moveHighlighters.forEach(function (value) {
               value.setAttributeNS(null, "visibility", "hidden");
            });
        }
    };

    this.clearPieces = function () {
        pieces.forEach(function (piece) {
            piece.parentNode.removeChild(piece);
        });
        pieces = [];
    };

    this.registerBoardClickCallback = function (cb) {
        boardClickCallback = cb;
    };
};
