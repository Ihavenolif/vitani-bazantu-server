const express = require("express")
const app = express()
cors = require("cors")
bodyParser = require("body-parser")
const expressWs = require("express-ws")(app)

app.use(cors())
app.use(bodyParser.urlencoded({ extended: false}))
app.use(bodyParser.json())

let client = null

app.get("/", function (req, res) {
    console.log(req.socket.remoteAddress)

    if(client){
        client.send("get request received")
    }

    res.send("Hello World")
})

app.post("/pripsat_body", function (req, res) {
    input = req.body

    client.send(JSON.stringify(input))
})

app.ws("/", function (ws, req) {
    client = ws
    console.log("connection opened")

    ws.on("close", () => {
        console.log("Connection closed")
    })
})

const PORT = 6969

app.listen(PORT, function () {
    console.log("Server is running on port " + PORT + ". Hit CTRL+C to stop.");
})