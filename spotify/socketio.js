const app = require('express')(); 
const express = require('express'); 
const server = require('http').Server(app);
const io = require('socket.io')(server);

// * Server 

const port = 3000;

app.get('/', (req,res) => {
  	res.sendFile(__dirname +'/public/index.html');		});

app.use('/static', express.static('public'))

server.listen(port, () =>  {
  	console.log(`Server is runnign port ${port} `);		});


// * Socket.io

io.on('connection', client => {
	
	console.log(' new socket connection ', client.id );
	io.emit('msg','say hello to the world');
	// * Sockets

	client.on('msg', data => { 
		console.log('socket-msg : ', data);
	});

	client.on('disconnect', () => { 
		console.log(' socket disconnected ');
	});

	// 	**	  Eo socket.io
});
