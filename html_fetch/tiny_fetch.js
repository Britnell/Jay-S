const https = require("https");
const fetch = require("node-fetch");
const htmlparser = require("node-html-parser");
const fs = require("fs");

fs.readFile("tinyhtml.txt", "utf8", function (err, data) {
  if (err) throw err;
  console.log(" read tiny txt ");
  tiny_desk(data);
});

function tiny_desk(html) {
  let pos = 0;

  let videos = [];

  while (pos != -1) {
    // * find by id="video-title"
    let vid = {};
    // get title
    let ti = html.indexOf('id="video-title"', pos); // index of title

    if (ti != -1) {
      let ta = html.indexOf(">", ti) + 1;
      let tb = html.indexOf("<", ta);
      let title = html.slice(ta, tb);
      // remove NL & spaces
      title = title.replace(/(\r\n|\n|\r)/gm, " ");
      title = title.replace(/\s+/g, " ");
      if (title[0] == " ") title = title.slice(1);
      if (title[title.length - 1] == " ")
        title = title.slice(0, title.length - 1);
      //
      vid.title = title;

      // href =
      let hi = html.lastIndexOf("href=", ti);
      let ha = html.indexOf("?v=", hi) + 3;
      let hb = html.indexOf("&amp", ha);
      vid.href = html.slice(ha, hb);
      //
      videos.push(vid);
      pos = ti + 1;
    } else {
      pos = ti;
    }

    // Eo loop
  }

  console.log(videos);

  console.log(" saving ");
  var savefile = fs.createWriteStream("tiny_links.txt");

  savefile.on("error", function (err) {
    /* error handling */
  });

  savefile.write("var tiny_links = \n[\n");
  videos.forEach(function (v) {
    savefile.write(JSON.stringify(v) + ",\n");
  });
  savefile.write("\n]\n");

  savefile.end();

  // Eo main
}

function get_video(html, after) {
  let title = html.indexOf("pl-video-title-link", after);
  if (title != -1) {
    let beg = html.lastIndexOf("<a", title);
    let end = html.indexOf("</a>", title);
    let part = html.slice(beg, end);
    return { a: part, end: end };
  } else return { a: "", end: -1 };
}

function get_link(heading) {
  let href = heading.indexOf("href=");
  let beg = heading.indexOf('"', href);
  let end = heading.indexOf('"', beg + 1);
  let link = heading.slice(beg + 1, end);
  if (href == -1 || beg == -1 || end == -1) return -1;
  else return link;
}

function get_tag(html, tag, after) {
  let beg = html.indexOf("<" + tag, after);
  let end = html.indexOf("</" + tag + ">", beg);
  let part = html.slice(beg, end + ("</" + tag + ">").length);
  if (beg == -1 || end == -1) return ["", -1];
  else return [part, end];
}
