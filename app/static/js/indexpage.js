function growNav() {
  document.querySelector(".sidebar").style.width =
    "15%";
}
function shrinkNav() {
  document.querySelector(".sidebar").style.width =
    "4%";
}

function revealHidden() {
  const hiddenText =
    document.querySelectorAll(".hidden");
  hiddenText.forEach((el) =>
    el.classList.add("reveal")
  );
}

function hideHidden() {
  const hiddenText =
    document.querySelectorAll(".hidden");
  hiddenText.forEach((el) =>
    el.classList.remove("reveal")
  );
}

function incrementLike() {
  let likeCount = 0;
  const likeCountDisplay =
    document.getElementById("likeCount");
  likeCount++;
  likeCountDisplay.textContent = likeCount;
}

function currentPosts() {
  var curr = document.getElementById("current");
  var save = document.getElementById("saved");
  var prev = document.getElementById("previous");
  curr.style.display = "grid";
  save.style.display = "none";
  prev.style.display = "none";
}

function savedPosts() {
  var curr = document.getElementById("current");
  var save = document.getElementById("saved");
  var prev = document.getElementById("previous");
  curr.style.display = "none";
  save.style.display = "grid";
  prev.style.display = "none";
}

function previousPosts() {
  var curr = document.getElementById("current");
  var save = document.getElementById("saved");
  var prev = document.getElementById("previous");
  curr.style.display = "none";
  save.style.display = "none";
  prev.style.display = "grid";
}