//

const iframe = document.getElementById("iframe");
// console.log(iframe);

function random_article() {
  let r = Math.floor(Math.random() * links.length);
  iframe.src = links[r];
  // console.log(" R: ", r, links[r]);

  //
}

document.getElementById("clickbutton").onclick = function () {
  random_article();
};

random_article();
