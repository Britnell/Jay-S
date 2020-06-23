//

// const iframe = document.getElementById("iframe");
const iframe = document.getElementsByTagName("iframe")[0];

console.log(tiny_links);

function random_desk() {
  let r = Math.floor(Math.random() * tiny_links.length);
  let link = iframe.src;
  let x = link.lastIndexOf("/") + 1;
  link = link.slice(0, x);
  iframe.src = link + tiny_links[r].href;
  console.log("iframe : ", iframe.src, " > ", link, " +  ", r, tiny_links[r]);
  // iframe.src = links[r];

  //
}

document.getElementById("clickbutton").onclick = function () {
  random_desk();
};

random_desk();
