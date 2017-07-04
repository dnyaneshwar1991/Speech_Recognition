var http = require('http');
var express = require('express');
var request = require('request');
var app = express(); 
var    bodyParser = require('body-parser');
//http://localhost:3000/_getproduct/8821264 


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


//app.use(bodyParser.text({ type: 'text/html' }))


	

/*	var path1 = "compute/" + keys[0];	
	var options = {
    		host: 'localhost',
    		path:  path1,
    		method: 'get',
    		port: 8085,	
    		headers: { 'Content-Type': 'application/x-www-form-urlencoded'}
     };
	 //console.log("options are ready");
  	 var req = http.request(options, function(res) {
  	 	res.setEncoding('utf8');
  	 	res.on('data', function (TempCommand) {
    			console.log('response from python library: ' + TempCommand);
                });

          });

      req.on('error', function(e) {
   	 console.log(e);
 	 });

      // Write the audio data in the request body.
     
      //var dt = "{'resData':'"+command+"'}";
      //console.log(dt);
      req.write();
      //console.log("command 2:",command);
      req.end();

      });
        
*/

//support parsing of application/x-www-form-urlencoded post data
app.use(bodyParser.urlencoded({ extended: true }));

app.post('/_getproduct', function(req, res) {
	console.log("body:", req.body);
        var keys =Object.keys(req.body); 
        console.log(keys[0]);


request.get({ url: "http://localhost:8085/compute/" + keys[0]},      function(error, response, body) { 
              if (!error && response.statusCode == 200) { 
                  //res.json(body);
	          console.log(body);
		  res.json(body); 
                 } 

             });   
        });
     


app.listen(3000, function () {
  console.log('Example app listening on port 3000!')
}); 
