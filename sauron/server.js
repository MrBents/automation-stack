var express = require('express');
var body_parser = require("body-parser");
var app = express();
var http = require('http').Server(app);
var io = require('socket.io')(http);
var spawn = require("child_process").spawn;
var fs = require('fs');
var toArray = require('stream-to-array')
var pythonProcess;


app.use(express.static(__dirname + '/public'));
app.use(body_parser.json()); //
app.use(body_parser.urlencoded({
    extended: true
})); // to allow for req.body

io.on("connection", (socket) => {
    console.log("socket connected");
});

// Handler
app.get('/script', (req, res) => {
    console.log('received');
    res.sendStatus(200);
    // req.data.pipe(fs.createWriteStream('./public/img.jpg')).then(() => {
    //     res.sendStatus(200);
    // })
    // pythonProcess = spawn('python', ["./pyscripts/script.py", 1, 2]);
    // pythonProcess.stdout.on('data', function(data) {
    //     let j = data.toString('utf8');
    //     console.log(JSON.stringify(j));
    // });
    // res.sendStatus(200);
});

app.post('/image', (req, res) => {

    console.log('received photo');
    toArray(req, (data) => {
        console.log(data);
    })
    // var bufs = [];
    // req.on('data', function(d) {
    //     bufs.push(d);
    // });
    // req.on('end', function() {
    //     var buf = Buffer.concat(bufs);
    //     fs.writeFile(`./public/dynamic_imgs/img${Math.random()*100}.jpg`, buf, function(err) {
    //         if (err) {
    //             return console.log(err);
    //         }
    //
    //         console.log("The file was saved!");
    //         res.sendStatus(200);
    //     });
    // });

    // req.on('end', () => {
    //     fs.writeFile(`./public/dynamic_imgs/img${Math.random()*100}.jpg`, data, function(err) {
    //         if (err) {
    //             return console.log(err);
    //         }
    //
    //         console.log("The file was saved!");
    //     });
    //     res.sendStatus(200);
    // })
    // req.data.pipe(fs.createWriteStream(`./public/dynamic_imgs/img${Math.random()*100}.jpg`)).then(() => {
    //     // io.emit("image");
    // });
});

app.get('/get_path', (req, res) => {
    res.send(path);
})





var server = http.listen(3000, () => {
    console.log("server is listening on port", server.address().port);
});

// io.emit('message', req.body);