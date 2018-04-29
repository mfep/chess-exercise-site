var ChessBoard = function() {
    const xmlns = "http://www.w3.org/2000/svg";
    const TILE = 50;
    const PIECE_SCALE = 1.1;

    var tiles = [];
    var pieces = [];
    var svgnode = document.getElementById("chess-board");
    var boardClickCallback = function(san) { console.log(san) };

    function createRectGroupClicked (x, y) {
        return function (mouseEv) {
            var target = mouseEv.target;
            while (target.getAttribute("class") !== "rectGroup") {
                target = target.parentElement;
            }
            var san = String.fromCharCode(97 + x) + (8 - y).toString();
            boardClickCallback(san);
        }
    }

    this.drawBoard = function () {
        svgnode.setAttributeNS(null, "width", (8 * TILE).toString());
        svgnode.setAttributeNS(null, "height", (8 * TILE).toString());

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

        // tiles
        for (var y = 0; y < 8; y++) {
            var row = [];
            for (var x = 0; x < 8; x++) {
                var color = (9 * y + x) % 2 ? "#af6336" : "#fcfa9f";
                var rectGroup = addRect(x * TILE, y * TILE, TILE, TILE, color);
                rectGroup.onclick = createRectGroupClicked(x, y);
                row.push(rectGroup);
            }
            tiles.push(row);
        }
    };

    this.drawPieces = function (chessGame) {
        function addPiece(row, col, piece) {
            var pieceElem = document.getElementById(piece).cloneNode(true);
            pieceElem.removeAttribute("id");
            pieceElem.setAttributeNS(null, "transform", "scale(" + PIECE_SCALE + ")");
            tiles[row][col].appendChild(pieceElem);
            return pieceElem;
        }

        this.clearPieces();
        var boardAscii = chessGame.ascii();
        boardAscii = boardAscii.replace(/ /g, '');
        var lines = boardAscii.split("\n");
        for (var y = 0; y < 8; ++y) {
            for (var x = 0; x < 8; ++x) {
                var char = lines[y+1].charAt(x+2);
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
                    pieces.push(addPiece(y, x, color+"-"+figure));
                }
            }

        }
    };

    this.clearPieces = function () {
        pieces.forEach(function (piece) {
            piece.parentNode.removeChild(piece);
        });
        pieces = [];
    };
};
