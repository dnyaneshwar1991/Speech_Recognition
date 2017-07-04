var express = require('express');
var request = require('request');
var http = require('http');
var fs = require('fs');
var app = express();
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

//support parsing of application/json type post data
//app.use(bodyParser.json());

//support parsing of application/x-www-form-urlencoded post data
//app.use(bodyParser.urlencoded({ extended: true }));

app.use(bodyParser.raw({ type: 'audio/wav', limit: '50mb' }));
app.post('/postUsers', function (req, res) {
//TempCommand('text');
      var data = req.body;
     // console.log(req.body);
			
	  var options = {
    		host: 'localhost',
    		path: '/hello',
    		method: 'POST',
    		port: 8081,	
    		headers: { 'Content-Type': 'audio/wav' }
                        };
   
  	 var req = http.request(options, function(res) {
  	 	res.setEncoding('utf8');
  	 	res.on('data', function (chunk){

		
		TempCommand(chunk);

		

  			});
                        });
  	
	
  	 
      req.on('error', function(e) {
   	    console.log(e);
 	   });

  // Write the audio data in the request body.
  req.write(data);
  req.end();				        	

})


/* write ur func here */


function TempCommand(command){
	//console.log(" in func TempCommand() ");
	 console.log("command",command); 
       
         var options = {
    		host: 'localhost',
    		path:  '/_getproduct',
    		method: 'post',
    		port: 3000,	
    		headers: { 'Content-Type': 'application/x-www-form-urlencoded'}
     };
	 //console.log("options are ready");
  	 var req = http.request(options, function(res) {
  	 	res.setEncoding('utf8');
  	 	res.on('data', function (TempCommand) {
    			console.log('BODY: ' + TempCommand);
                });

          });

      req.on('error', function(e) {
   	 console.log(e);
 	 });

      // Write the audio data in the request body.
     
      //var dt = "{'resData':'"+command+"'}";
      //console.log(dt);
      req.write(command);
      //console.log("command 2:",command);
      req.end();

 }

/*  


//http://localhost:8086/_getproduct/8821264
app.get('/_getproduct/:id', function(req, res) {
       if (!req.params.id) {
           res.status(500);
           res.send({"Error": "Looks like you are not senging the product id to get the product details."});
           console.log("Looks like you are not senging the product id to get the product detsails.");
       }
      request.get({ url: "http://localhost:3000/_getproduct/energy%20consumption%20on%2015%20april%202018" + req.params.id },      function(error, response, body) {
              if (!error && response.statusCode == 200) {
                  res.json(body);
                 }
             });
     });

*/

app.listen(8086, function () {
  console.log('Example app listening on port 8086!')
});









 
