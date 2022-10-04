const TABLE = document.getElementById("table")
const IP = "gvnqrkod.cz"
let pole = []

function generateTable(){
    document.body.style.zoom="50%"
    for(y = 0; y < 250; y++){ //ITERACE NA DVOUROZMĚRNÉM POLI
        pole[y] = []
        row = table.insertRow(y) 
        for(x = 0; x < 250; x++){ 
            pole[y][x] = row.insertCell(x)
            //PŘIDÁNÍ KLIKATELNÉHO DIV ELEMENTU, KTERÝ PŘI KLIKNUTÍ ZAVOLÁ FUNKCI tah() SÁM NA SEBE
            pole[y][x].innerHTML = "<div class=\"policko\" id=\"" + y + "," + x + "\" onclick=\"tah(pole[" + y + "][" + x + "], " + y + ", " + x + ")\"></div>"
            pole[y][x].red = 254
            pole[y][x].green = 254
            pole[y][x].blue = 254
        }
    }
    window.addEventListener("mousedown", mouseDownHandler)
    requestInitialData()
}

window.selectHand = () =>{
    TABLE.classList.add("hand")
}

window.unselectHand = () => {
    TABLE.classList.remove("hand")
}

ele = window

let pos = { top: 0, left: 0, x: 0, y: 0 };

const mouseDownHandler = function (e) {
    if(parent.MENU.contentWindow.mode != "hand") return
    e.preventDefault()
    pos = {
        // The current scroll
        left: ele.scrollX,
        top: ele.scrollY,
        // Get the current mouse position
        x: e.clientX,
        y: e.clientY,
    };

    document.addEventListener('mousemove', mouseMoveHandler);
    document.addEventListener('mouseup', mouseUpHandler);
}

const mouseMoveHandler = function (e) {
    // How far the mouse has been moved
    const dx = e.clientX - pos.x;
    const dy = e.clientY - pos.y;

    // Scroll the element
    ele.scroll(pos.left - dx, pos.top - dy)
    ele.scrollTop = pos.top - dy;
    ele.scrollLeft = pos.left - dx;
}

const mouseUpHandler = function () {
    document.removeEventListener('mousemove', mouseMoveHandler);
    document.removeEventListener('mouseup', mouseUpHandler);
}

function requestInitialData(){
    xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = () =>{
        if(xhttp.readyState == 4 && xhttp.status == 200){
            for(x of JSON.parse(LZString.decompressFromUTF16(xhttp.responseText))){
                drawSquare(x)
            }
        }
    }
    xhttp.open("POST", "http://" + IP + ":6969/getInitialDrawings", true)
    xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8")
    xhttp.send(JSON.stringify({kokot: 12}))
}

function componentToHex(c) {
    const hex = c.toString(16);
    return hex.length == 1 ? "0" + hex : hex;
}
  
function rgbToHex(r, g, b) {
    return "#" + componentToHex(r) + componentToHex(g) + componentToHex(b);
}

function tah(pole, y, x){
    if(parent.MENU.contentWindow.mode == "hand") return
    if(parent.MENU.contentWindow.mode == "brush"){
        color = parent.MENU.contentWindow.color
        square = document.getElementById(y + "," + x)
        square.style.border = "1px solid " + color
        square.style.backgroundColor = color
        sendPixelInfo({
            x: x,
            y: y,
            color: color,
            border: color
        })
        return
    }
    if(parent.MENU.contentWindow.mode == "eraser"){
        square = document.getElementById(y + "," + x)
        square.style.border = "1px solid #999"
        square.style.backgroundColor = "#FEFEFE"
        sendPixelInfo({
            x: x,
            y: y,
            color: "#FEFEFE",
            border: "#999"
        })
        return
    }
    if(parent.MENU.contentWindow.mode == "colorpicker"){
        const square = document.getElementById(y + "," + x)
        
        if(!square.style.backgroundColor){
            parent.MENU.contentWindow.setColor("#ffffff")
            return
        }

        if(square.style.backgroundColor == "black"){
            parent.MENU.contentWindow.setColor("#000000")
            return
        }

        const rgbFunc = square.style.backgroundColor
        const red = rgbFunc.split(",")[0].substring(4)
        const green = rgbFunc.split(",")[1].substring(1)
        const blue = rgbFunc.split(",")[2].substring(1, rgbFunc.split(",")[2].length-1)

        parent.MENU.contentWindow.setColor(rgbToHex(Number(red), Number(green), Number(blue)))
        return
    }
}

function sendPixelInfo(object){
    /*xhttp = new XMLHttpRequest()
    xhttp.open("POST", "http://" + IP + ":6969/draw", true)
    xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8")
    xhttp.send(JSON.stringify(object))*/
    socket.send(JSON.stringify(object))
}

function drawSquare(pixelInfo){
    square = document.getElementById(pixelInfo.y + "," + pixelInfo.x)

    square.style.backgroundColor = pixelInfo.color
    square.style.border = "1px solid " + pixelInfo.border
}

window.scaleTable = function(value){
    value = parseFloat(value)

    transformValue = ((value - 1)/(2 * value))*100

    TABLE.style.transform = "translate(" + transformValue  + "%, " + transformValue + "%)"
    TABLE.style.scale = value
    
    const tableContainer = document.getElementById("table-container")

    tableContainer.style.width = (12*250 * value).toString() + "px"
    tableContainer.style.height = (12*250 * value).toString() + "px"
}

generateTable()

const socket = new WebSocket("ws://" + IP + ":6969")

socket.addEventListener("open", (event) => {
    console.log("connected successfully")
})

socket.addEventListener("close", (event) => {
    parent.showDisconnectedPopup()
})

socket.addEventListener("message", (event) => {
    drawSquare(JSON.parse(event.data))
})