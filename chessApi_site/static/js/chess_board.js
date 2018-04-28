const xmlns = "http://www.w3.org/2000/svg";
const TILE = 50;

function drawBoard() {
    var svgnode = document.getElementById("chess-board");
    svgnode.setAttributeNS(null, "width", (8*TILE).toString());
    svgnode.setAttributeNS(null, "height", (8*TILE).toString());

    function addRect(x, y, w, h, color) {
        var rectElem = document.createElementNS(xmlns, "rect");
        rectElem.setAttributeNS(null, "x", x);
        rectElem.setAttributeNS(null, "y", y);
        rectElem.setAttributeNS(null, "width", w);
        rectElem.setAttributeNS(null, "height", h);
        rectElem.setAttributeNS(null, "fill", color);
        svgnode.appendChild(rectElem);
    }

    // background
    addRect(0, 0, 8*TILE, 8*TILE, "#fcfa9f");

    // tiles
    for (var y = 0; y < 8; y++) {
        for (var x = 0; x < 8; x++) {
            if ((9 * y + x) % 2 === 0) {
                addRect(x*TILE, y*TILE, TILE, TILE, "black");
            }
        }
    }
}

window.onload = drawBoard;
