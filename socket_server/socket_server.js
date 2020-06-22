/*
    # # # # ------------   
*/



	// * Setup
	const express = require('express'); // running immediately

    const app = require('express')(); // running immediately
  const server = require('http').Server(app);
const io = require('socket.io')(server);

  //  ***   Server

const port = 8000;
app.use(express.static('public'));

// app.use('/static', express.static('public') );

server.listen(port, () =>  {
  console.log(`Server is runnign port ${port} `);
});

// app.get('/', (req,res) => {
//   res.sendFile(__dirname +'/public/index.html');
// });
// app.get('/socket', (req,res) => {
//   res.sendFile(__dirname +'/public/socket.html');
// });
// app.get('/airbar', (req,res) => {
//   res.sendFile(__dirname +'/public/airbar.html');
// });

// app.get('/lamp', (req,res) => {
//   res.sendFile(__dirname +'/public/lamp_rgb.html');
// });


	// *  Socket

// const exampleSpace = io.of('/example'); 
// exampleSpace.on('connection', (socket)=>{

io.on('connection', (socket)=>{
    // socket refers to client side obj / event
  console.log(`New user connected :  \tSocket id \t ${socket.id} ` );
  
  if(false){
    console.log("Starting timer");
    var interval = setInterval(function() {   
    //console.log("Interval : Swap!");
    }, 200);  
  }

  socket.on('msg', (msg)=>{
  	console.log(` #msg :\t${msg}.`);
  	io.emit('msg', msg);
  });

  socket.on('airbar', (data)=>{
    // console.log(`  ~~ airbar :\t${data}.`);
    io.emit('airbar', data );
  });
  
  socket.on('lamp', (data)=>{
    // broadcast / fwd lamp packages
    io.emit('lamp', data );
  });

  socket.on('disconnect',()=>{
  	console.log(' # # User disconnected.');
  	io.emit('message', ' # user disconnected # ' );
  });

});

