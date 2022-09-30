const TABLE = document.getElementById("table")
const IP = "gvnqrkod.cz:5000"
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
    requestInitialData()
}

function requestInitialData(){
    console.log("ioeguiwhoiguh")
    xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = () =>{
        if(xhttp.readyState == 4 && xhttp.status == 200){
            console.log("request received back")
            for(x of JSON.parse(xhttp.responseText)){
                drawSquare(x)
            }
        }
    }
    xhttp.open("POST", "http://" + IP + ":6969/getInitialDrawings", true)
    xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8")
    xhttp.send(JSON.stringify({kokot: 12}))
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

    console.log("square-received")
    console.log(square)

    square.style.backgroundColor = pixelInfo.color
    square.style.border = "1px solid " + pixelInfo.border
}

window.scaleTable = function(value){
    value = parseFloat(value)

    transformValue = ((value - 1)/(2 * value))*100

    TABLE.style.transform = "translate(" + transformValue  + "%, " + transformValue + "%)"
    TABLE.style.scale = value
    
}

generateTable()

const socket = new WebSocket("ws://" + IP + ":6969")

socket.addEventListener("open", (event) => {
    alert("Connected successfully")
})

socket.addEventListener("message", (event) => {
    drawSquare(JSON.parse(event.data))
})