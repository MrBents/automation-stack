var express = require('express');
var body_parser = require("body-parser");
var app = express();
var http = require('http').Server(app);
var io = require('socket.io')(http);
var spawn = require("child_process").spawn;
var pythonProcess;


app.use(express.static(__dirname));
app.use(body_parser.json()); //
app.use(body_parser.urlencoded({
    extended: false
})); // to allow for req.body

io.on("connection", (socket) => {
    console.log("socket connected");
});

// Handler
app.get('/script', (req, res) => {
    pythonProcess = spawn('python', ["./pyscripts/script.py", 1, 2]);
    pythonProcess.stdout.on('data', (data) => {
        let j = data.toString('utf8');
        console.log(j);
    });
    res.sendStatus(200);
});

app.get('start_testing', (req, res) => {
  pythonProcess = spawn('python', ["./pyscripts/sensors.py"]);

});




var server = http.listen(3000, () => {
    console.log("server is listening on port", server.address().port);
});

// io.emit('message', req.body);
