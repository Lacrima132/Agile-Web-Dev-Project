function growNav() {
  document.querySelector(".sidebar").style.width =
    "15%";
}
function shrinkNav() {
  document.querySelector(".sidebar").style.width =
    "4%";
}
function currentPosts() {
  var curr = document.getElementById("current");
  var work = document.getElementById("working");
  var prev = document.getElementById("previous");
  curr.style.display = "grid";
  work.style.display = "none";
  prev.style.display = "none";
}

function workingPosts() {
  var curr = document.getElementById("current");
  var work = document.getElementById("working");
  var prev = document.getElementById("previous");
  curr.style.display = "none";
  work.style.display = "grid";
  prev.style.display = "none";
}

function previousPosts() {
  var curr = document.getElementById("current");
  var work = document.getElementById("working");
  var prev = document.getElementById("previous");
  curr.style.display = "none";
  work.style.display = "none";
  prev.style.display = "grid";
}