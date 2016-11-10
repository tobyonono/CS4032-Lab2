var server = require("ws").createServer();
var studentnum = 12312156;
var IP = require("ip");
var address= IP.address();

server.listen(8000, function(){
	console.log("Listening: ")
});

server.on('connection', function(socket){
	console.log('New Connection');

	socket.on("text", function(str)
	{
		if(str === 'KILL_SERVICE\n')
		{
			console.log(message);
			socket.destroy();
		}


		else if(str === 'HELO text\n')
		{
			socket.write("HELO text\n" + "IP: " + address + "\nPort: " + 
				"8000" + "\nStudentID: " + studentnum);

			console.log(message);
			socket.end();
		}

		else
		{
			socket.write(str.toUpperCase()+" && other")

		}

		console.log("Received " +str)

	});

	socket.on("close", function(code, reason)
	{
		console.log("Connection closed")
	});

});