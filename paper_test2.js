// Only executed our code once the DOM is ready.

  /* Global Scope

        When code is executed as PaperScript, the script’s scope is populated
        with all fields of the currently active PaperScope object, which within
        the script appear to be global.

        In a JavaScript context, only the paper variable is added to the global
        scope, referencing the currently active PaperScope object, through which
        all properties and Paper.js classes can be accessed.

  */

function on_load(){
  if(dataReady){
    console.log(" DATA :", numbers );
  }
  else{
    console.log("data unready ");
  }
  //
}
on_load();

// * Test draw

var path1 = new Path({
  strokeWidth: 0,
  strokeColor: 'blue',
  strokeCap: 'round',
  selected: true
});
path1.strokeColor = 'black';
path1.moveTo(view.center-100);
path1.lineTo(view.center);

// from angle
var angl = new Point({
    length: 10,
    angle: 90
  });

// random
var random_point = new Point.random() * view.size;
var random_var = Math.random() * 256;

// * Symbol
var path = new Path.Star(new Point(0,0), 5, 8, 16);
path.style = {
  fillColor: 'yellow',
  strokeColor: 'blue'
}
var symbol = new SymbolDefinition(path);
var placed = symbol.place();
placed.position = view.center;

//console.log(path1.getLastSegment().getPoint() );

// * Frame Draw
function onFrame(event){
  // event.count = number of times event fired
  path1.rotate(0.5, view.center );
  placed.position = path1.getFirstSegment().getPoint();
}

// Click
function onClick(){
}

function onMouseDown(){
}
function onMouseDrag(){
}
function onMouseUp(){
}

// Move
function onMouseMove(){
}

// * Keyboard
function onKeyDown(){
}

function onKeyUp(){
}
