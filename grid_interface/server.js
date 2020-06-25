

const express = require('express')
const app = express()

app.get('/', function (req, res) {

  res.sendFile(__dirname +'/public/ctrl_interface1.html');
})


// app.use(express.static('public'))		// localhost:3000/filename > /public/filename
app.use('/static', express.static('public'))

app.listen(3000, function () {
  console.log('Node listening on port 3000');
});
