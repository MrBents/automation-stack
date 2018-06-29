var express = require('express');
var body_parser = require("body-parser");
var app = express();
var http = require('http').Server(app);
var io = require('socket.io')(http);
var spawn = require("child_process").spawn;
var fs = require('fs');
var pythonProcess;


app.use(express.static(__dirname + '/public'));
app.use(body_parser.json()); //
app.use(body_parser.urlencoded({
    extended: false
})); // to allow for req.body

io.on("connection", (socket) => {
    console.log("socket connected");
});

// Handler
app.post('/script', (req, res) => {
    req.data.pipe(fs.createWriteStream('./public/img.jpg')).then(() => {
        res.sendStatus(200);
    })
    // pythonProcess = spawn('python', ["./pyscripts/script.py", 1, 2]);
    // pythonProcess.stdout.on('data', function(data) {
    //     let j = data.toString('utf8');
    //     console.log(JSON.stringify(j));
    // });
    // res.sendStatus(200);
});





var server = http.listen(3000, () => {
    console.log("server is listening on port", server.address().port);
});

// io.emit('message', req.body);