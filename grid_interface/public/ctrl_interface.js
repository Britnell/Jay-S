// Only executed our code once the DOM is ready.
paper.install(window);

var grid = [];


window.onload = function()
{
      // * Setup Paper
    paper.setup('paperCanvas');
    var ui = new Tool();


    // ** Gridding

    var mag_ref, wx, wy, NW, NH;


    function create_grid(W,H)
    {
      NW = W;      NH = H;

      wx = paper.view.size.width  /(W+1);
      wy = paper.view.size.height /(H+1);
      var id=0;

      // reference for distance between dots
      mag_ref = new Point(wx/2.5,wy/2.5).length;

      for(var y=0; y<H; y++){
        for( var x=0; x<W; x++){
          let gridpoint = { 
            'id': id,
            'id2': y*W+x,
            'x': x,
            'y': y,
            'pos': new Point(x*wx+wx, y*wy+wy)
          }
          
          grid.push(gridpoint);

          id++;

          // Eo double for
        }
      }
    }

    function draw_grid(){
      grid.forEach(function(x,i){
        let dot = Shape.Circle({
          center: x.pos,
          radius: 5,
          fillColor: 'blue'
        });

      });
    }

    

    function closest_point(pos){
      
      let px = (pos.x -wx) /wx;
      let py = (pos.y-wy) /wy;
      let pid = Math.round(py)*NW +Math.round(px);
      if(pid<grid.length && pid>=0)
        return pid;
      // Eo func
    }

    // ** Begin

    var cursor = Shape.Circle({
          center: [-10,-10],
          radius: 15,
          strokeColor: 'red',
          strokeWidth: 5
        });

    create_grid(10,10);

    draw_grid();
    
    console.log( 'DIM = ', [NW,NH] ,'   w = ', [wx,wy],'  ref', mag_ref);
    
    console.log( '600 : ',  closest_point(new Point(600,600) ) );
    
    var dragL = 0;
    var dragIndex=[];
    var dragLine = new Path({
      strokeColor: 'green',
      strokeWidth: 8,
      closed: false
    });

    ui.onMouseDown = function(event){
      console.log(' new drag : ', dragIndex, dragLine );

      let clo = closest_point(event.point);

      if(clo){
        dragIndex = [];
        dragIndex.push( grid[clo] );
        dragLine.removeSegments();
        dragLine.add( grid[clo].pos );
        dragL = 1;
        // if closest
      }

      console.log( ' drag : ', dragIndex);
      //
    }

    ui.onMouseDrag = function(event) {
      let clo = closest_point(event.point);
      if(clo){
        if(clo != dragIndex[dragL-1].id){
          dragIndex.push( grid[clo] );
          dragLine.add( grid[clo].pos );
          dragL++;
        }
        // if closest
      }
      // 
    }

    ui.onMouseUp = function(event){
      
      // 
    }

    ui.onMouseMove = function(event){
      let id = closest_point(event.point);
      if(id){
        cursor.position = grid[id].pos;
      }
      // Eo mouse move
    }

    function onFrame(event){
      


      // Eo onFrame
    }

    // Window onload
}