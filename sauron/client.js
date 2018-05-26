var express = require('express');
var body_parser = require("body-parser");
var app = express();
var http = require('http').Server(app);
var io = require('socket.io')(http);