var express = require('express');
var body_parser = require("body-parser");
var app = express();
var http = require('http').createServer(app);
var io = require('socket.io')(http);
var spawn = require("child_process").spawn;
var fs = require('fs');
const fileUpload = require('express-fileupload');
var pythonProcess;
const axios = require('axios');


app.use(express.static(__dirname + '/public'));
app.use(body_parser.json()); //
app.use(body_parser.urlencoded({
    extended: false
})); // to allow for req.body
app.use(fileUpload());
// app.use(express.static('public'))


io.on("connection", (socket) => {
    console.log("socket connected");
});


// Handler
app.get('/script', (req, res) => {
    console.log('received');
    console.log(res)
    console.log(req);
    //res.sendStatus(200);
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
let current_path;
let countgobriel = 0;
var input_arr = [];
app.post('/image', async (req, res) => {

    console.time(`${countgobriel} someFunction`);
    current_path = `dynamic_imgs/img${countgobriel}.jpg`;
    let image = req.files.image;
    var cl = await getClassification(image);
    console.log(cl.data);
    countgobriel++;

    input_arr.push(current_path);
    if(input_arr.length > 4)
      input_arr = input_arr.slice(-5,);

    image.mv(`./public/dynamic_imgs/img${countgobriel}.jpg`, function(err) {
    if (err)
      return res.status(500).send(err);
    io.emit('image');
    res.send('File uploaded!');
    });
});

app.get('/get_path', (req, res) => {
    res.send({'path' : current_path , 'lista': input_arr});
})

async function getClassification(image) {
  console.log('gobriel');
  // console.log(image)
  // const formData = new FormData()
  const config = {
            headers: { 'content-type': 'multipart/form-data' }
  }
  var response = await axios.post('http://localhost:5000/image', image);
  return response
}



var server = http.listen(3000, () => {
    console.log("server is listening on port", server.address().port);
});

// io.emit('message', req.body);
