const express = require("express")
const app = express()
cors = require("cors")
bodyParser = require("body-parser")
const fs = require("fs")
const LZString = require("./lz-string-node")

let gamesRemaining = 12;

/**
 * @type {String}
 */
const dataString = fs.readFileSync("./result_json.json", "utf-8")

/**
 * @type {Array<Array<String>>}
 */
const data = JSON.parse(dataString)


app.use(cors())
app.use(bodyParser.urlencoded({ extended: false}))
app.use(bodyParser.json())

app.get("/", function (req, res) {
    console.log(req.socket.remoteAddress)

    res.send(String(gamesRemaining--))
})

app.post("/getMap", function (req, res) {
    res.send(LZString.compressToUTF16(dataString))
})

const PORT = 6969

app.listen(PORT, function () {
    console.log("Server is running on port " + PORT + ". Hit CTRL+C to stop.");
})