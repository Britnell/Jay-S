

//    ****      Authorization

// * Check the URL for Token

const hash = window.location.hash
.substring(1)
.split('&')
.reduce(function (initial, item) {
  if (item) {
    var parts = item.split('=');
    initial[parts[0]] = decodeURIComponent(parts[1]);
  }
  return initial;
}, {});

//window.location.hash = '';

// Set token
var spotify = new SpotifyWebApi();
let _token = hash.access_token;
const authEndpoint = 'https://accounts.spotify.com/authorize';
const client = '6ec357e821234793a037258fa7554168';
const redirectUri = 'https:%2F%2Fwebs.wonday.eu%2Fhtml%2Fspotify_playlist.html';
const scopes = [
  'user-read-email',
  //' user-read-recently-played',' user-read-currently-playing',' user-read-playback-state',' user-modify-playback-state',' app-remote-control', // ' playlist-read-collaborative'
];

// * If there is no token, redirect to Spotify authorization

if (!_token) {
  $('#prelogin').show();
  //$('#login').click();
}
else {
  // * LETS START
  // console.log("TOKENNN", $('#postlogin'), $('#prelogin') );
  spotify.setAccessToken(_token);
  $('#postlogin').show();
  get_playlists();
}

//https://developer.spotify.com/documentation/web-api/reference
//https://www.npmjs.com/package/spotify-web-api-js
var listdata=[];
var requests, errors, features;


function get_playlists(){
  // prep
  $('#subhead')[0].innerHTML = `Choose your playlist :`;

  // Get users playlists
  // GET  /v1/me/playlists  Get a List of Current User's Playlists  playlists
  //
  spotify.getUserPlaylists()  // note that we don't pass a user id
    .then(function(data)
    {
        data.items.map(function(playlists) {
           //let item = $(``<li>` + artist.name + '</li>');
           let item = $(`<li class="playlistitem" onclick="get_list('${playlists.id}')"> ${playlists.name} </li>`);
           item.appendTo($('#userlists'));
         });
    }, function(err) {
      console.error(err);
    });

  // Eo function
}

function get_list(id){

  // Get a playlist's tracks
  //  * GET https://api.spotify.com/v1/playlists/{playlist_id}  (/tracks)
  //  * https://developer.spotify.com/documentation/web-api/reference/playlists/get-playlist/
  $('#userlists')[0].innerHTML='';
  $('#subhead')[0].innerHTML = '';
  listdata = [];
  no_error = true;

  // * get first 100 tracks
  spotify.getPlaylist(id)
  .then(function(data) {
    // * analyse playlist
      console.log(" playlist : \n", data );
      errors = 0;
      features = 0;

       // * for each track
       requests = ( data.tracks.total < 100 ) ? data.tracks.total : 100;

       for(var x=0; x<requests; x++){
         if(!data.tracks.items[x].is_local){
           // exclude local files
           var tr = new Object();
           tr.nr = x;
           tr.track = data.tracks.items[x].track;
           tr.id = tr.track.id;
               // track.features = get_features(track.id);
           listdata.push(tr);
           get_analysis(tr.id, x);
           // let lis = $(`<li> ${tr.track.name} </li>`);
           // lis.appendTo($('#playlist'));
         }
         else{
           listdata.push("");
           errors++;
         }
       }
       console.log(" requested all data..");
       //console.log(" \n\nFinished fetching Playlist Data # # # #\n\n", listdata );
       wait_for_data();

  }, function(err) {
    console.error(err);
  });
  //
}


function get_analysis(trackId, listId)
{
  spotify.getAudioFeaturesForTrack(trackId).then(function(data){
    listdata[listId].sound = data;
    features++;
  },
  function(err){
    errors++;
    no_error = false;
  });
  // Eo get analysis
}

function wait_for_data()
{
  if(errors + features < requests )
  {
    // console.log(` timer....\tD: ${requests}\t Res: ${features} & Err: ${errors} `);
    setTimeout(wait_for_data, 300);
  }
  else{
    // console.log(` Data : ${requests}\t Res: ${features} & Err: ${errors} `);
    all_the_data();
  }
  // -
}

var keys = ['C', 'C#', 'D','D#','E','F','F#','G','G#','A','A#','B'];

function read_track_features(track){
  //  **  Audio Features    **    https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/

  // * Acousticness  - confidence track is acoustic ,  mainly = 0 or not, use binary
  var ac = track.sound.acousticness;
  if(ac < 0.1 )        track.acoustic = 0;
  else                 track.acoustic = Math.round(ac*100);

  // * Instrumental  - Predicts whether a track contains no vocals >0.5 ~~instrumental
  // if(track.sound.instrumental < 0.2)       track.instrumental = 'vocals';
  // else //if(track.sound.instrumental > 0.5)  
  track.instrumental = Math.round(track.sound.instrumentalness*100);

  // * liveness      - Detects the presence of an audience in the recording.  >0.8 ~ live
  if(track.sound.liveness > 0.8)        track.liveness = true;
  else if(track.sound.liveness < 0.2 )   track.liveness = false;

  // * speechiness   - spoken word   >0.33 may contain both music and speech     >0.66  are probably made entirely of spoken words.
    // if(track.sound.speechiness > 0.66 )          track.speech = 100;
    // else if(track.sound.speechiness > 0.33 )      track.speech = 50;
    // else                                           track.speech = 0;
  track.speech = Math.round(track.sound.speechiness*100)

  // * valence       - describing the musical positiveness   positive : happy, cheerful, euphoric  // negative : sad, depressed, angry
  track.valence = Math.round(track.sound.valence*100);

  // * Danceability  - leaning normal distrib ~2/3   // tempo, rhythm stability, beat strength, and overall regularity
  track.dance = Math.round(track.sound.danceability*100);

  // * Energy        - // fast, loud, noisy   : { dynamic range, perceived loudness, timbre, onset rate, and general entropy }
  track.energy = Math.round(track.sound.energy*100);

  // * loudness      - in dB     0 to -60 dB
  if(track.sound.loudness > 13 )             track.loudness = 'loud';
  else if(track.sound.loudness > 25 )        track.loudness = 'normal';
  else                                       track.loudness = 'quiet';

  track.key = keys[track.sound.key];
  if(track.sound.mode==0)       track.keym = 'maj';
  else if(track.sound.mode==1)  track.keym = 'min';

  track.tempo = track.sound.tempo;
  track.popularity = track.track.popularity;
  track.explicit = track.track.explicit;
  track.duration = Math.floor(track.track.duration_ms/1000);
  track.name = track.track.name;
  track.artists = track.track.artists[0].name;
  for(var a=1; a<track.track.artists.length; a++)
    track.artists += ", "+track.track.artists[a].name;

  track.sample = track.track.preview_url;
  track.trackURL = track.track.external_urls.spotify;
  track.album = track.track.album;

  // track.artistsObj = track.track.artists;

  // delete track['sound'];
  // delete track['track'];

  // Eo track
}

//const svg = d3.create("svg").attr("viewBox", [0, 0, width, height]);
//var svg = d3.select("body").append("svg").attr("height","800").attr("width","100%");
var svg = d3.select("body");

function all_the_data()
{
  console.log( " All requests resolved " );

  var x=0;
  while(x<listdata.length){
    var tr = listdata[x];
    if(tr){
        read_track_features(tr);
        x++;
    }
    else{
      console.log("splice : ", x, tr);
      listdata.splice(x,1);
    }
  }

  console.log("after cleanup ", listdata[0] );

  write_table(listdata); 

  // Eo all the data there
}


function write_table(list)
{
    let header = $('<tr id="listheader"> </tr>');
      header.appendTo('#playlisttable');

    $('<th>Track</th>').appendTo('#listheader');
    $('<th>Artist</th>').appendTo('#listheader');
    $('<th>Release</th>').appendTo('#listheader');
    $('<th>Sample</th>').appendTo('#listheader');
    $('<th>Popular</th>').appendTo('#listheader');         
    $('<th>Key</th>').appendTo('#listheader');
    $('<th>Tempo</th>').appendTo('#listheader');
    $('<th>Energy</th>').appendTo('#listheader');
    $('<th>Danceability</th>').appendTo('#listheader');
    // $('<th>Loudness</th>').appendTo('#listheader');
    $('<th>Valence</th>').appendTo('#listheader');
    $('<th>Acoustic</th>').appendTo('#listheader');
    $('<th>Instrumental</th>').appendTo('#listheader');
    $('<th>Speech</th>').appendTo('#listheader');
    $('<th>Live</th>').appendTo('#listheader');
    $('<th>Explicit</th>').appendTo('#listheader');

    for( var t=0; t<list.length; t++)
    {
      // create a row per track
      let trackrow = $(`<tr id="pl${t}">  </tr>`);
      trackrow.appendTo($('#playlisttable'));

      let name = $(`<td><a href="${list[t].trackURL}">${list[t].name}</a></td>`);
        name.appendTo($(`#pl${t}`));
      let artist = $(`<td>${list[t].artists}</td>`);
        artist.appendTo($(`#pl${t}`));
      let release = $(`<td>${list[t].album.release_date}</td>`);
        release.appendTo($(`#pl${t}`));
      let sample = $(`<a href="${list[t].sample}">sample</a>`);
        sample.appendTo($(`#pl${t}`));
      let pop = $(`<td><div style="width:${list[t].popularity}%;" class="bar pop">${list[t].popularity}</div></td>`);
        pop.appendTo($(`#pl${t}`));
      let key = $(`<td>${list[t].key} ${list[t].keym}</td>`);
        key.appendTo($(`#pl${t}`));
      let tempo = $(`<td>${Math.round(list[t].tempo)}</td>`);
        tempo.appendTo($(`#pl${t}`));
      let energy = $(`<td><div style="width:${list[t].energy}%;" class="bar">${list[t].energy}</div></td>`);
        energy.appendTo($(`#pl${t}`));
      let dance = $(`<td><div style="width:${list[t].dance}%;" class="bar">${list[t].dance}</div></td>`);
        dance.appendTo($(`#pl${t}`));
      // let loud = $(`<td>${list[t].loudness}</td>`);
      //   loud.appendTo($(`#pl${t}`));
      let positive = $(`<td><div style="width:${list[t].valence}%;" class="bar positive">${list[t].valence}</div></td>`);
        positive.appendTo($(`#pl${t}`));
      let acoustic = $(`<td><div style="width:${list[t].acoustic}%;" class="bar acoustic">${list[t].acoustic}</div></td>`);
        acoustic.appendTo($(`#pl${t}`));
      let instrum;
      if(list[t].instrumental<10)        
        instrum = $(`<td><div style="width:0%;" class="bar">vocals</div></td>`);
      else        instrum = $(`<td><div style="width:${list[t].instrumental}%;" class="bar">${list[t].instrumental}</div></td>`);
      // instrum = $(`<td><div style="width:0%;" class="bar">${list[t].instrumental}</div></td>`);
      instrum.appendTo($(`#pl${t}`));
      let speech = $(`<td><div style="width:${list[t].speech}%;" class="bar speech">${list[t].speech}</div></td>`);
        speech.appendTo($(`#pl${t}`));
      let live;
      if(list[t].liveness===true)
        live = $(`<td><div style="width:100%;" class="bar liveness">Live</div></td>`);
      else //if(list[t].liveness===false)
        live = $(`<td><div style="width:0%;" class="bar liveness">no</div></td>`);
      //else        live = $(`<td><div style="width:0%;" class="bar liveness">Undefined</div></td>`);
      live.appendTo($(`#pl${t}`));
      let explic;
      if(list[t].explicit)            explic = $(`<td><div style="width:100%;" class="bar">Explicit</div></td>`);
      else                            explic = $(`<td></td>`);
      explic.appendTo($(`#pl${t}`));
      
        
    }

    // Eo
}

function fwd_to_login(){
  window.location = `${authEndpoint}?client_id=${client}&redirect_uri=${redirectUri}&scope=${scopes.join('%20')}&response_type=token&show_dialog=true`;
}


// -----------------------------------------------------------------------------

// d3.select("#playlist")
  // svg.select("#playlist")
  //   .data(listdata)
  //   .enter().append("tspan")
  //     .text(function(l) { return " "+l.nr+": " + l.name + " - " +l.artists; })
  //     .attr("font-size","14")
  //     .attr("y", function(d,i){ return 0 + 20*i; })
  //     .attr("x", 100);
