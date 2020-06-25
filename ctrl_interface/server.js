

const express = require('express')
const app = express()

app.get('/', function (req, res) {
  // console.log("server : ", req, res );
  // res.send('Hello World')
  res.sendFile(__dirname +'/public/ctrl_gsap.html');
})


// app.use(express.static('public'))		// localhost:3000/filename > /public/filename
app.use('/static', express.static('public'))

app.listen(3000, function () {
  console.log('Node listening on port 3000')
})
