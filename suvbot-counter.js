const express = require("express")
const app = express()
cors = require("cors")

let gamesRemaining = 12;

app.use(cors())

app.get("/", function (req, res) {
    res.send(String(gamesRemaining--))
})

app.get("/checkCount", function (req, res) {
    res.send(String(gamesRemaining))
})

app.get("/setCount", function (req, res) {
    if(!req.query.count) res.send("Invalid data");
    count = Number(req.query.count)
    gamesRemaining = count;
    res.send(String(count))
})

const PORT = 6969

app.listen(PORT, function () {
    console.log("Server is running on port " + PORT + ". Hit CTRL+C to stop.");
})