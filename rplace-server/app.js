const express = require("express")
const app = express()
cors = require("cors")
bodyParser = require("body-parser")
const expressWs = require("express-ws")(app)
const fs = require("fs")
const LZString = require("./lz-string-node")

app.use(cors())
app.use(bodyParser.urlencoded({ extended: false}))
app.use(bodyParser.json())

let clients = []
let pixelChanges = []

function removeClientFromList(ws){
    for(x in clients){
        if(clients[x] && clients[x].ws == ws){
            clients[x] = undefined
        }
    }

    temp = []
    for(x of clients){
        if(x) temp.push(x)
    }

    clients = temp
}

app.get("/", function (req, res) {
    console.log(req.socket.remoteAddress)

    res.send("Hello World")
})

app.post("/getInitialDrawings", function (req, res) {
    res.send(LZString.compressToUTF16(JSON.stringify(pixelChanges)))
})

app.ws("/", function (ws, req) {
    clients.push(ws)
    console.log("connection opened")

    ws.on("message", (msg) => {
        pixelChanges.push(JSON.parse(msg))

        fs.appendFileSync("./backups/drawing_data.txt", msg + ";\n")

        for(x of clients){
            x.send(msg)
        }
    })

    ws.on("close", () => {
        removeClientFromList(ws)
        console.log("Connection closed")
    })
})

const PORT = 6969

app.listen(PORT, function () {
    console.log("Server is running on port " + PORT + ". Hit CTRL+C to stop.");
})