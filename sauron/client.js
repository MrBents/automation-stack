var express = require('express');
var body_parser = require("body-parser");
var app = express();
var http = require('http').Server(app);
var io = require('socket.io')(http);


app.use(express.static(__dirname));
app.use(body_parser.json()); //
app.use(body_parser.urlencoded({
    extended: false
})); // to allow for req.body

io.on("connection", (socket) => {
    console.log("socket connected");
});


var server = http.listen(3000, () => {
    console.log("server is listening on port", server.address().port);
});