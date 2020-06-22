

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
const redirectUri = 'http:%2F%2Flocalhost:3000%2Fstatic%2Falbums_implicit.html';
// const redirectUri = 'https:%2F%2Fwebs.wonday.eu%2Fhtml%2Fspotify_playlist.html';
// const redirectUri = 'file:%2F%2F%2FUsers%2Fthomas.britnelldesignaffairs.com%2FDocuments%2Falbums_implicit.html';

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
  
  album_page();

  // *
}

//https://developer.spotify.com/documentation/web-api/reference
//https://www.npmjs.com/package/spotify-web-api-js
var listdata=[];
var requests, errors, features;


function fwd_to_login(){
  window.location = `${authEndpoint}?client_id=${client}&redirect_uri=${redirectUri}&scope=${scopes.join('%20')}&response_type=token&show_dialog=true`;
}


function album_page()
{
  

  // Eo func
}






