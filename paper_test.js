// Only executed our code once the DOM is ready.
paper.install(window);

window.onload = function()
{
      // * Setup Paper
    paper.setup('paperCanvas');
    var ui = new Tool();


    //view.draw();
    var strokes = new Group();
    var path;

    ui.onMouseDown = function(event){
      path = new Path();
      strokes.addChild(path);
      path.strokeColor = 'black';
      path.add(event.point);
      // view.draw();
    }

    ui.onMouseDrag = function(event) {
      path.add(event.point);
      path.smooth();
      // view.draw();
    }

    ui.onMouseUp = function(event){
      // strokes.addChild(path);
      console.log( strokes.children );
    }

    function onFrame(event){



      // Eo onFrame
    }


    // * socket setup
    /*
    const socket = io();
    socket.on('connect', ()=>{
      //
      socket.emit('message', 'Hi its picture frame, im ready');
      //
      var path1 = new Path();
      path1.strokeColor = 'black';
      var start = new Point(100, 100);
      path1.moveTo(start);
      path1.lineTo(start.add([ 200, -50 ]));
    });

      // Socket / Receive
    socket.on('message', (data)=>{
      console.log(`socket: ${data}`);
    });

    socket.on('swap', (data)=>{
      var dist = 500;
      var rp = Point.random();
      var newp = new Point( rp.x *dist, rp.y *dist );
      console.log(`socket:  $swap : ${data} , p:${rp}  // ${newp}.`);

      var circl = new Path.Circle( {
        center: newp,
        radius: 1,
        fillColor: 'blue'
        });
    });
    */
}
