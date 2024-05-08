document.addEventListener("DOMContentLoaded", (e) => {
  const splash = document.querySelector(".splash");
  if (window.location.pathname === "/frontend/home.html") {
    // Lock scrolling
    document.body.style.overflow = "hidden";
    if (splash) {
      jumbleText();
      setTimeout(() => {
        splash.classList.add("hideSplash");
        document.body.style.overflow = "auto";
      }, 3500);
    }
  }
});

document.addEventListener("DOMContentLoaded", function () {
  if (window.location.pathname === "/frontend/home.html") {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          console.log(entry);
          if (entry.isIntersecting) {
            entry.target.classList.add("reveal");
          } else {
            entry.target.classList.remove("reveal");
          }
        });
      },
      {
        rootMargin: "-50% 0px",
      }
    );

    const scrollElements = document.querySelectorAll(".scroll");
    scrollElements.forEach((el) => observer.observe(el));
  }
});

document.addEventListener("DOMContentLoaded", togglePostVisibility);

function growNav() {
  document.querySelector(".sidebar").style.width = "15%";
}
function shrinkNav() {
  document.querySelector(".sidebar").style.width = "4%";
}

function revealHidden() {
  const hiddenText = document.querySelectorAll(".hidden");
  hiddenText.forEach((el) => el.classList.add("reveal"));
}

function hideHidden() {
  const hiddenText = document.querySelectorAll(".hidden");
  hiddenText.forEach((el) => el.classList.remove("reveal"));
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

function jumbleText() {
  const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
  let iterations = 0;

  const interval = setInterval(() => {
    const jumbleElement = document.querySelector(".jumble");
    if (!jumbleElement) {
      clearInterval(interval);
      return;
    }

    jumbleElement.innerText = jumbleElement.innerText
      .split("")
      .map((letter, index) => {
        if (index < iterations) {
          return jumbleElement.dataset.value[index];
        }

        return letters[Math.floor(Math.random() * 26)];
      })
      .join("");

    if (iterations >= 9) clearInterval(interval);
    iterations += 1 / 10;
  }, 30);
}

function togglePostVisibility() {
  const postBubbles = document.querySelectorAll(".postbubble");

  postBubbles.forEach((postBubble) => {
    postBubble.addEventListener("mouseenter", function () {
      const postText = this.querySelector(".posttext");
      const reactBar = this.querySelector(".reactbar");
      postText.style.opacity = "1";
      reactBar.style.opacity = "1";
    });

    postBubble.addEventListener("mouseleave", function () {
      const postText = this.querySelector(".posttext");
      const reactBar = this.querySelector(".reactbar");
      postText.style.opacity = "0";
      reactBar.style.opacity = "0";
    });
  });
}
let likeSelected = false;
let dislikeSelected = false;

function toggleLike(elementId, iconId, isLike) {
  const countDisplay = document.getElementById(elementId);
  const icon = document.getElementById(iconId);
  let count = parseInt(countDisplay.textContent);

  if (isLike) {
    if (!likeSelected) {
      count++;
      icon.classList.remove("fa-thumbs-o-up");
      icon.classList.add("fa-thumbs-up");
      likeSelected = true;

      if (dislikeSelected) {
        dislikeSelected = false;
        const dislikeIcon = document.getElementById("dislikeIcon");
        dislikeIcon.classList.remove("fa-thumbs-down");
        dislikeIcon.classList.add("fa-thumbs-o-down");
        document.getElementById("dislikeCount").textContent--;
      }
    } else {
      count--;
      icon.classList.remove("fa-thumbs-up");
      icon.classList.add("fa-thumbs-o-up");
      likeSelected = false;
    }
  } else {
    if (!dislikeSelected) {
      count++;
      icon.classList.remove("fa-thumbs-o-down");
      icon.classList.add("fa-thumbs-down");
      dislikeSelected = true;

      if (likeSelected) {
        likeSelected = false;
        const likeIcon = document.getElementById("likeIcon");
        likeIcon.classList.remove("fa-thumbs-up");
        likeIcon.classList.add("fa-thumbs-o-up");
        document.getElementById("likeCount").textContent--;
      }
    } else {
      count--;
      icon.classList.remove("fa-thumbs-down");
      icon.classList.add("fa-thumbs-o-down");
      dislikeSelected = false;
    }
  }

  countDisplay.textContent = count;
}

document.addEventListener("DOMContentLoaded", function () {
  const filterItems = document.querySelectorAll(".filter-item");
  const filterTagsContainer = document.getElementById("filterTagsContainer");

  filterItems.forEach(function (item) {
    item.addEventListener("click", function () {
      const filterName = this.dataset.filter;
      addFilterTag(filterName);
    });
  });

  function addFilterTag(filterName) {
    const filterTag = document.createElement("div");
    filterTag.classList.add("filter-tag");
    filterTag.innerHTML = `
          <i class="fa fa-times filterTagClose" aria-hidden="true"></i>
          ${filterName}
      `;
    filterTagsContainer.appendChild(filterTag);
  }

  // Add event listener to the filter tags container to handle click events on close icons
  filterTagsContainer.addEventListener("click", function (event) {
    if (event.target.classList.contains("filterTagClose")) {
      // If the clicked element is a close icon, remove its parent (the filter tag)
      const filterTag = event.target.parentElement;
      filterTag.remove();
    }
  });
});
