const express = require("express")
const app = express()
cors = require("cors")
bodyParser = require("body-parser")
const expressWs = require("express-ws")(app)

app.use(cors())
app.use(bodyParser.urlencoded({ extended: false}))
app.use(bodyParser.json())

let clients = []
let pixelChanges = []

app.get("/", function (req, res) {
    console.log(req.socket.remoteAddress)

    res.send("Hello World")
})

app.post("/getInitialDrawings", function (req, res) {
    res.send(JSON.stringify(pixelChanges))
})

app.ws("/", function (ws, req) {
    clients.push(ws)
    console.log("connection opened")

    ws.on("message", (msg) => {
        pixelChanges.push(JSON.parse(msg))

        for(x of clients){
            x.send(msg)
        }
    })

    ws.on("close", () => {
        console.log("Connection closed")
    })
})

const PORT = 6969

app.listen(PORT, function () {
    console.log("Server is running on port " + PORT + ". Hit CTRL+C to stop.");
})