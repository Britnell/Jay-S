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
}