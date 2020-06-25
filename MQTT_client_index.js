


  	// * Setup
  	const express = require('express'); // running immediately
  	const path = require('path');

      const app = require('express')(); // running immediately
    const server = require('http').Server(app);
    var port = 8080;

    // const io = require('socket.io')(server);

// *    Inits

server.listen(port, () =>  {
  console.log(`Server is runnign port ${port} `);
  //-
});


	// * Express

app.get('/', (req,res) => {
  res.sendFile(__dirname +'/public/index.html');
});

app.use(express.static('public'));


//  *   MQTT

function MQTT_subscribe(client, chnlname)
{
  client.subscribe(chnlname, function (err) {
      if (!err) {
        console.log(`subscribed to '${chnlname}' channel.`)
        client.publish(chnlname, 'Hello channel.');
        // THIS message does come back because we subscribed to topic 'test'
      }
  });
}

const mqtt = require('mqtt');
var mqt_serv = '192.168.86.2';
var client  = mqtt.connect('mqtt://'+mqt_serv );

client.on('error',(err)=>{
    console.log("[mqtt] error : ", err);
    client.end();
});

client.on('connect', ()=>{
    console.log("[mqtt] : connect client connected! ");
    console.log("subscribing");
    MQTT_subscribe(client, 'message');
    MQTT_subscribe(client, 'esp_button_1');
    // io.emit('message','MQTT-server connected');
    // * Eo connect
});
 
client.on('message', function (topic, message) {
    if(topic=='message') {
      console.log(`[MQTT-message]:\tMSG:${message.toString()}` );
    }
    else if(topic=='esp_button_1'){
      console.log(`[MQTT-message]:\t${topic.toString()}:${message.toString()}` );
    }
    //
});


client.on('close',()=>{
  console.log('mqtt client disconnected');
  //
});


// var interval = setInterval(function() {   // save to var so can clear later
//   //process.stdout.write(`waiting ${currentTime/1000} seconds`);    // repeating printout
//   //console.log("Interval : ping");
//   //socket.emit('swap', 'NOW');
//   broker.publish(message, function() {
//     console.log('ping');
//     });
  // }, 30000);


// **
