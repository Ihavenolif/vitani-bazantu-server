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
let chatClients = []
let pixelChanges = []
let messages = []

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

function removeChatClientFromList(ws){
    for(x in chatClients){
        if(chatClients[x] && chatClients[x].ws == ws){
            chatClients[x] = undefined
        }
    }

    temp = []
    for(x of chatClients){
        if(x) temp.push(x)
    }

    chatClients = temp
}

app.get("/", function (req, res) {
    console.log(req.socket.remoteAddress)

    res.send("Hello World")
})

app.post("/getInitialDrawings", function (req, res) {
    res.send(LZString.compressToUTF16(JSON.stringify(pixelChanges)))
})

app.post("/getChatHistory", function (req, res) {
    res.send(LZString.compressToUTF16(JSON.stringify(messages)))
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

app.ws("/chat", function (ws, req) {
    chatClients.push(ws)
    console.log("connection opened")

    ws.on("message", (msg) => {
        messages.push(JSON.parse(msg))
        // XSS VULN

        fs.appendFileSync("./backups/messages.txt", msg + ";\n")

        for(x of chatClients){
            x.send(msg)
        }
    })

    ws.on("close", () => {
        removeChatClientFromList(ws)
        console.log("Connection closed")
    })
})

const PORT = 6969

app.listen(PORT, function () {
    console.log("Server is running on port " + PORT + ". Hit CTRL+C to stop.");
})