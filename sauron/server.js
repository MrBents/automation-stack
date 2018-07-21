var express = require('express');
var body_parser = require("body-parser");
var app = express();
var http = require('http').createServer(app);
var io = require('socket.io')(http);
var spawn = require("child_process").spawn;
var fs = require('fs');
const fileUpload = require('express-fileupload');
var pythonProcess;
const config = require('./config');
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
let new_Crop_path;
let nombre_img;
let tag_img;
let gP;
let bP;
let tag_img_error;

var input_arr = [];
// var countFiles = require('count-files');
// var stats = countFiles(dir, function (err, results) {
//   countgobriel = results.files
// })


app.post('/image', async (req, res) => {
    res.sendStatus(200)
    var date0 = Date.parse(Date())
    // console.time(`${countgobriel} someFunction`);
    current_path = `img${countgobriel}.jpg`;
    let image = req.files.image;
    await saveImg(image);
    // console.log(req.files);
    var img_name = await getClassification(config.IMG_ABS_PATH + current_path);
    var get_info = (img_name.data).split('_');
    nombre_img = String(get_info[0]);
    tag_img = String(get_info[1]);

    tag_img_error = String(get_info[2]);
    // console.log(tag_img_error);
    gP = String(get_info[3]);
    bP = String(get_info[4]);
    new_Crop_path = String(config.IMG_NEW_PATH + nombre_img + '_' + tag_img + '_' + tag_img_error + '.jpg');
    // console.log('gg');
    // console.log(get_info[2])
    // console.console.log();(Date.parse(get_info[2]))
    // console.log(date2 - date1)
    // console.log(date1 - date2)
    // console.log(Date.now())
    // console.log(Date.parse(Date()))
    // console.log(get_info1.slice(1,2))
    // console.log(get_info1.slice(2,3))

    // input_arr.push(current_path);
    // if(input_arr.length > 4)
    //   input_arr = input_arr.slice(-5,);

    // res.send(img_name.data);

});

app.get('/get_path', (req, res) => {
    res.send({'path' : (String(new_Crop_path)) , 'name': nombre_img, 'tag': tag_img, 'errortag': tag_img_error, 'goodp' : gP, 'badp' : bP});
})


function saveImg(image) {
    return new Promise((resolve, reject) => {
        image.mv(config.IMG_ABS_PATH + `img${countgobriel++}.jpg`, function(err) {

        if (err)
          reject(err)
        else {
          io.emit('image');
          resolve();
        }
      });
    });
}


async function getClassification(_path) {
  // console.log('gobriel');
  // console.log(image)
  // const formData = new FormData()
  // const config = {
  //           headers: { 'content-type': 'multipart/form-data' }
  // }
  var response = await axios.post('http://localhost:5000/image', {
    path : _path
  });
  return response
}



var server = http.listen(3000, () => {
    console.log("server is listening on port", server.address().port);
});

// io.emit('message', req.body);
