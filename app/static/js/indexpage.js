document.addEventListener(
  "DOMContentLoaded",
  (e) => {
    const splash =
      document.querySelector(".splash");
    console.log(window.location.pathname);
    if (
      sessionStorage.getItem(
        "splashScreenSeen"
      ) === null
    ) {
      if (
        window.location.pathname === "/" ||
        window.location.pathname === "/home"
      ) {
        splash.classList.remove("invis");
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
      sessionStorage.setItem(
        "splashScreenSeen",
        "true"
      );
    }
  }
);

document.addEventListener(
  "DOMContentLoaded",
  function () {
    if (
      window.location.pathname === "/" ||
      window.location.pathname === "/home"
    ) {
      const observer = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            console.log(entry);
            if (entry.isIntersecting) {
              entry.target.classList.add(
                "reveal"
              );
            } else {
              entry.target.classList.remove(
                "reveal"
              );
            }
          });
        },
        {
          rootMargin: "-50% 0px",
        }
      );

      const scrollElements =
        document.querySelectorAll(".scroll");
      scrollElements.forEach((el) =>
        observer.observe(el)
      );
    }
  }
);

document.addEventListener(
  "DOMContentLoaded",
  togglePostVisibility
);

function growNav() {
  document.querySelector(".sidebar").style.width =
    "16rem";
}
function shrinkNav() {
  document.querySelector(".sidebar").style.width =
    "5rem";
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
    const jumbleElement =
      document.querySelector(".jumble");
    if (!jumbleElement) {
      clearInterval(interval);
      return;
    }

    jumbleElement.innerText =
      jumbleElement.innerText
        .split("")
        .map((letter, index) => {
          if (index < iterations) {
            return jumbleElement.dataset.value[
              index
            ];
          }

          return letters[
            Math.floor(Math.random() * 26)
          ];
        })
        .join("");

    if (iterations >= 9) clearInterval(interval);
    iterations += 1 / 10;
  }, 30);
}

function togglePostVisibility() {
  const postBubbles = document.querySelectorAll(
    ".postbubble"
  );

  postBubbles.forEach((postBubble) => {
    postBubble.addEventListener(
      "mouseenter",
      function () {
        const postText =
          this.querySelector(".posttext");
        const reactBar =
          this.querySelector(".reactbar");
        postText.style.opacity = "1";
        reactBar.style.opacity = "1";
      }
    );

    postBubble.addEventListener(
      "mouseleave",
      function () {
        const postText =
          this.querySelector(".posttext");
        const reactBar =
          this.querySelector(".reactbar");
        postText.style.opacity = "0";
        reactBar.style.opacity = "0";
      }
    );
  });
}

let likeSelected = false;
let dislikeSelected = false;

function toggleLike(button) {
  const likeContainer = button.parentElement; // Get parent container
  console.log("parent =" + likeContainer);

  const likeCountDisplay =
    likeContainer.querySelector(
      ".reactnumber:nth-child(2)"
    ); // Like count
  console.log("count =" + likeCountDisplay);

  let likeIcon = likeContainer.querySelector(
    ".fa-thumbs-o-up"
  ); // Like icon (solid)
  console.log("icon =" + likeIcon);
  if (likeIcon == null) {
    likeSelected = true;
    likeIcon = likeContainer.querySelector(
      ".fa-thumbs-up"
    ); // Like icon (outline)
    console.log("icon2 =" + likeIcon);
  } else {
    likeSelected = false;
  }
  console.log("like status =" + likeSelected);

  const dislikeCountDisplay =
    likeContainer.querySelector(
      ".reactnumber:nth-child(4)"
    ); // Dislike count
  console.log("count2 =" + dislikeCountDisplay);

  let dislikeIcon = likeContainer.querySelector(
    ".fa-thumbs-o-down"
  ); // Dislike icon (solid)
  console.log("icon3 =" + dislikeIcon);
  if (dislikeIcon == null) {
    dislikeSelected = true;
    dislikeIcon = likeContainer.querySelector(
      ".fa-thumbs-down"
    ); // Dislike icon (outline)
    console.log("icon4 =" + dislikeIcon);
  } else {
    dislikeSelected = false;
  }
  console.log(
    "dislike status =" + dislikeSelected
  );

  const isLike =
    button.classList.contains("like"); // Check if like button
  console.log("like =" + isLike);

  let likeCount = parseInt(
    likeCountDisplay.textContent
  );
  console.log("likeCount =" + likeCount);
  let dislikeCount = parseInt(
    dislikeCountDisplay.textContent
  );
  console.log("dislikeCount =" + dislikeCount);

  // Like logic
  if (isLike) {
    if (!likeSelected) {
      likeCount++;
      likeIcon.classList.add("fa-thumbs-up");
      likeIcon.classList.remove("fa-thumbs-o-up"); // Remove outline if present
      likeSelected = true;

      if (dislikeSelected) {
        dislikeSelected = false;
        dislikeCount--;
        dislikeIcon.classList.add(
          "fa-thumbs-o-down"
        );
        dislikeIcon.classList.remove(
          "fa-thumbs-down"
        );
      }
    } else {
      likeCount--;
      likeIcon.classList.add("fa-thumbs-o-up");
      likeIcon.classList.remove("fa-thumbs-up");
      likeSelected = false;
    }
  } else {
    // Dislike logic
    if (!dislikeSelected) {
      dislikeCount++;
      dislikeIcon.classList.add("fa-thumbs-down");
      dislikeIcon.classList.remove(
        "fa-thumbs-o-down"
      ); // Remove outline if present
      dislikeSelected = true;

      if (likeSelected) {
        likeSelected = false;
        likeCount--;
        likeIcon.classList.add("fa-thumbs-o-up"); // Add outline back
        likeIcon.classList.remove("fa-thumbs-up");
      }
    } else {
      dislikeCount--;
      dislikeIcon.classList.add(
        "fa-thumbs-o-down"
      ); // Add outline back
      dislikeIcon.classList.remove(
        "fa-thumbs-down"
      );
      dislikeSelected = false;
    }
  }

  // Update DOM
  likeCountDisplay.textContent = likeCount;
  dislikeCountDisplay.textContent = dislikeCount;
}

document.addEventListener(
  "DOMContentLoaded",
  function () {
    // Your JavaScript code goes here
    const filterItems = document.querySelectorAll(
      ".filter-item"
    );
    const filterTagsContainer =
      document.getElementById(
        "filterTagsContainer"
      );

    filterItems.forEach(function (item) {
      item.addEventListener("click", function () {
        const filterName = this.dataset.filter;
        addFilterTag(filterName);
      });
    });

    function addFilterTag(filterName) {
      const filterTag =
        document.createElement("div");
      filterTag.classList.add("filter-tag");
      filterTag.innerHTML = `
        <i class="fa fa-times filterTagClose" aria-hidden="true"></i>
        ${filterName}
    `;
      filterTagsContainer.appendChild(filterTag);
    }

    // Add event listener to the filter tags container to handle click events on close icons
    filterTagsContainer.addEventListener(
      "click",
      function (event) {
        if (
          event.target.classList.contains(
            "filterTagClose"
          )
        ) {
          // If the clicked element is a close icon, remove its parent (the filter tag)
          const filterTag =
            event.target.parentElement;
          filterTag.remove();
        }
      }
    );
  }
);
