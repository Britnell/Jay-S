const https = require("https");
const fetch = require("node-fetch");
const htmlparser = require("node-html-parser");
const fs = require("fs");

function https_get(url, callback) {
  https.get(url, (res) => {
    res.setEncoding("utf8");
    let body = "";
    res.on("data", (data) => {
      body += data;
    });
    res.on("end", () => {
      callback(body);
    });
  });
}

let wiki_url = "https://en.wikipedia.org/wiki/Wikipedia:Unusual_articles";
const agent = new https.Agent({
  rejectUnauthorized: false,
});

fetch(wiki_url, { agent })
  .catch((err) => {
    console.log(" fetch-error-html : ", err);
  })
  .then((res) => res.text())
  .catch((err) => {
    console.log(" fetch error on text : ", err);
  })
  .then((res) => check_page(res))
  .catch((err) => {
    console.log(" fetch error on callback : ", err);
  });

function check_page(html) {
  // console.log(html);

  // * get body
  let body = get_tag(html, "body", 0)[0];
  // console.log(" body : ", body);

  // * find tables
  var tables = [];
  let pos = 0;

  while (pos != -1) {
    let tb = get_table(body, pos);
    if (tb[1] != -1) tables.push(tb[0]);
    pos = tb[1];
  }
  console.log(" tables ", tables.length);
  // parse_table(tables[0]);

  tables.forEach(function (table) {
    parse_table(table);
  });

  console.log(" links : ", links.length, " rows : ", rows, links[0]);

  var file = fs.createWriteStream("links.txt");
  file.on("error", function (err) {
    /* error handling */
  });
  links.forEach(function (l) {
    file.write("'" + l + "',\n");
  });
  file.end();
}

rows = 0;
links = [];

function parse_table(table) {
  // console.log(" #0 ", table);

  // loop through rows
  let pos = 0;
  while (pos != -1) {
    // row tag
    let tr = get_tag(table, "tr", pos);
    if (tr[1] != -1) {
      rows++;
      // td
      let bold = parse_row(tr[0]);
      // console.log(" bold : ", bold);
      if (bold != -1) {
        let link = "https://en.wikipedia.org" + get_link(bold);
        links.push(link);
      }
      // console.log(" link : ", link);
    }
    pos = tr[1];
  }
  //
}

function get_link(heading) {
  let href = heading.indexOf("href=");
  let beg = heading.indexOf('"', href);
  let end = heading.indexOf('"', beg + 1);
  let link = heading.slice(beg + 1, end);
  if (href == -1 || beg == -1 || end == -1) return -1;
  else return link;
}

function parse_row(tr) {
  // console.log(" tr : ", tr);
  // heading is <td><b>
  let beg = tr.indexOf("<td><b>");
  let end = tr.indexOf("</b>", beg);
  if (beg == -1 || end == -1) return -1;
  else return tr.slice(beg + 7, end);
}

function get_tag(html, tag, after) {
  let beg = html.indexOf("<" + tag, after);
  let end = html.indexOf("</" + tag + ">", beg);
  let part = html.slice(beg, end + ("</" + tag + ">").length);
  if (beg == -1 || end == -1) return ["", -1];
  else return [part, end];
}

function get_table(html, start) {
  let id = html.indexOf('class="wikitable"', start);
  let beg = html.indexOf("<tbody", id);
  let end = html.indexOf("</tbody>", beg);
  let part = html.slice(beg, end + 8);
  if (id == -1 || beg == -1 || end == -1) return ["", -1];
  else return [part, end];
}
