var express = require('express');
var request = require('request');
var app = express();
var fs = require("fs");
var sizeof = require('object-sizeof');
var http = require("http");
var FormData = require('form-data');

//require the body-parser nodejs module
var    bodyParser = require('body-parser');

//require the path nodejs module
var   path = require("path");

 
// Add headers
app.use(function (req, res, next) {

    // Website you wish to allow to connect
    res.header('Access-Control-Allow-Origin', '*');

    // Request methods you wish to allow
    res.header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, PATCH, DELETE');

    // Request headers you wish to allow
    res.header('Access-Control-Allow-Headers', 'Content-type');

    // Set to true if you need the website to include cookies in the requests sent
    // to the API (e.g. in case you use sessions)
    res.header('Access-Control-Allow-Credentials', true);

    // Pass to next layer of middleware
    next();
})

//app.use(bodyParser.raw);
app.use(bodyParser.raw({ type: 'audio/wav', limit: '50mb' }));


app.post('/hello', function (req, res) {
	
	//console.log("----------------------body:",req.body);
	//console.log("size:", req.body.length);
	
   var flag_for_wavfile = 0;
   var wav_str;
   var Command=''; 
 
    if (req.body.length)		// check for wavfile
	 {                    
		
		wav_str= req.body;
        
		fs.writeFile('sample_1.wav', wav_str, function(err) {
                        console.log(err ? 500 : 200 );
                        //res.send(err ? 500 : 200);
                     });
		flag_for_wavfile = 1;	
	 }

	else
	{
		flag_for_wavfile = 0;
		console.log("In else condition");
	}

	//res.send("Hi, Amol Gogawale");
	
	
	var formData = {
  		my_file: wav_str  //fs.createReadStream('/home/jjadhad/nodejs/test_20.wav')
	};
 
	request.post({url:'http://localhost:5000/stream/1' , formData: formData}, function(err, httpResponse, body) {
  		if (err) {
   	 return console.error('upload failed:', err);
  		}
  	   console.log('Upload successful!  Server responded with:', body);
	   console.log("body:",body);
	   Command = body;
	   console.log("Command:",Command);
	   res.send(body);
	});
			//console.log("body:",Command);
			//while(Command == 'undefined');
			//console.log("body:",Command);
			//res.send(Command);
			//return Command;
			
			
	
	})

    
	


var server = app.listen(8081, function () {

  //var host = server.address().address
  var port = server.address().port
  console.log("Listening on port:", port)

})
