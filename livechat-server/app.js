const express = require("express")
const app = express()
cors = require("cors")
bodyParser = require("body-parser")
const expressWs = require("express-ws")(app)

app.use(cors())
app.use(bodyParser.urlencoded({ extended: false}))
app.use(bodyParser.json())

let clients = []

app.get("/", function (req, res) {
    console.log(req.socket.remoteAddress)

    res.send("Hello World")
})

app.post("/send_message", function (req, res) {
    input = req.body

    for(x of clients){
        console.log(x)
        x.send(JSON.stringify(input))
    }
})

app.ws("/", function (ws, req) {
    clients.push(ws)
    console.log("connection opened")

    ws.on("close", () => {
        console.log("Connection closed")
    })
})

const PORT = 6996

app.listen(PORT, function () {
    console.log("Server is running on port " + PORT + ". Hit CTRL+C to stop.");
})