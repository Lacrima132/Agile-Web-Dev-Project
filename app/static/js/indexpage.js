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
		"17rem";
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

document
	.querySelectorAll(".dropdown")
	.forEach((dropdown) => {
		const menu =
			dropdown.querySelector(".drop-menu");

		dropdown.addEventListener(
			"mouseenter",
			() => {
				menu.style.display = "block";
				setTimeout(() => {
					menu.style.opacity = "1";
					menu.style.maxHeight = "500px";
				}, 10); // Small delay to trigger the transition
			}
		);

		dropdown.addEventListener(
			"mouseleave",
			() => {
				menu.style.opacity = "0";
				menu.style.maxHeight = "0";
				setTimeout(() => {
					menu.style.display = "none";
				}, 300); // Matches the CSS transition duration
			}
		);
	});

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

function goToPage(url) {
	window.location.href = url;
}

let likeSelected = false;
let dislikeSelected = false;

function toggleLike(button, postId) {
	const likeContainer = button.parentElement; // Get parent container
	console.log("parent =" + likeContainer);

	const likeCountDisplay =
		likeContainer.querySelector(
			".reactnumber:nth-child(2)"
		); // Like count
	let likeIcon = likeContainer.querySelector(
		".fa-thumbs-up, .fa-thumbs-o-up"
	); // Like icon
	const dislikeCountDisplay =
		likeContainer.querySelector(
			".reactnumber:nth-child(4)"
		); // Dislike count
	let dislikeIcon = likeContainer.querySelector(
		".fa-thumbs-down, .fa-thumbs-o-down"
	); // Dislike icon

	const isLike =
		button.classList.contains("like"); // Check if like button
	let url = `/like_post/${postId}`;
	if (!isLike) {
		url = `/dislike_post/${postId}`;
	}

	fetch(url, { method: "POST" })
		.then((response) => response.json())
		.then((data) => {
			if (data.success) {
				let likeCount = parseInt(
					likeCountDisplay.textContent
				);
				let dislikeCount = parseInt(
					dislikeCountDisplay.textContent
				);
				let likeSelected =
					likeIcon.classList.contains(
						"fa-thumbs-up"
					);
				let dislikeSelected =
					dislikeIcon.classList.contains(
						"fa-thumbs-down"
					);

				// Like logic
				if (isLike) {
					if (!likeSelected) {
						likeCount++;
						likeIcon.classList.add(
							"fa-thumbs-up"
						);
						likeIcon.classList.remove(
							"fa-thumbs-o-up"
						); // Remove outline if present
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
						likeIcon.classList.add(
							"fa-thumbs-o-up"
						);
						likeIcon.classList.remove(
							"fa-thumbs-up"
						);
					}
				} else {
					// Dislike logic
					if (!dislikeSelected) {
						dislikeCount++;
						dislikeIcon.classList.add(
							"fa-thumbs-down"
						);
						dislikeIcon.classList.remove(
							"fa-thumbs-o-down"
						); // Remove outline if present
						if (likeSelected) {
							likeSelected = false;
							likeCount--;
							likeIcon.classList.add(
								"fa-thumbs-o-up"
							); // Add outline back
							likeIcon.classList.remove(
								"fa-thumbs-up"
							);
						}
					} else {
						dislikeCount--;
						dislikeIcon.classList.add(
							"fa-thumbs-o-down"
						); // Add outline back
						dislikeIcon.classList.remove(
							"fa-thumbs-down"
						);
					}
				}

				// Update DOM
				likeCountDisplay.textContent = likeCount;
				dislikeCountDisplay.textContent =
					dislikeCount;
			} else {
				console.error(
					"Failed to update like/dislike status."
				);
			}
		})
		.catch((error) =>
			console.error("Error:", error)
		);
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

		if (filterTagsContainer) {
			filterItems.forEach(function (item) {
				item.addEventListener(
					"click",
					function () {
						const filterName =
							this.dataset.filter;
						addFilterTag(filterName);
					}
				);
			});

			function addFilterTag(filterName) {
				const filterTag =
					document.createElement("div");
				filterTag.classList.add("filter-tag");
				filterTag.innerHTML = `
        <i class="fa fa-times filterTagClose" aria-hidden="true"></i>
        ${filterName}
    `;
				filterTagsContainer.appendChild(
					filterTag
				);
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
		} else {
			console.warn(
				"Element with ID 'filterTagsContainer' not found. Script will not run on this page."
			);
		}
	}
);

function toggleUpdate(button, user_id) {
	var action =
		button.textContent === "Promoted"
			? "demote"
			: "promote";
	var newText =
		action === "promote"
			? "Promoted"
			: "Promote Me";

	// Change button text
	button.textContent = newText;

	// Perform fetch request
	fetch(`/promote_user/${user_id}`, {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify({ action: action }),
	})
		.then((response) => {
			if (response.ok) {
				return response.json(); // Parse the JSON response
			} else {
				throw new Error("Request failed");
			}
		})
		.then((data) => {
			if (data.success) {
				showMessage(
					action === "promote"
						? "User promoted successfully!"
						: "User demotion successful!"
				);
				document.getElementById(
					"promotionCount"
				).innerText = data.promotion_count; // Update promotion count
			} else {
				showMessage(
					"An error occurred. Please try again."
				);
			}
		})
		.catch((error) => {
			console.error(`Error ${action}ing:`, error);
			showMessage(
				"An error occurred. Please try again."
			);
		});

	console.log("Hello");
}

// Function to show flash messages
function showMessage(message) {
	var flashMessage =
		document.createElement("div");
	flashMessage.className = "flash-message";
	flashMessage.innerText = message;

	document.body.appendChild(flashMessage);

	// Remove the flash message after 3 seconds
	setTimeout(() => {
		flashMessage.remove();
	}, 3000);
}

document.addEventListener(
	"DOMContentLoaded",
	function () {
		const handleMouseMove = (e) => {
			const { currentTarget: target } = e;

			const rect = target.getBoundingClientRect(),
				x = e.clientX - rect.left,
				y = e.clientY - rect.top;
			target.style.setProperty(
				"--mouse-x",
				`${x}px`
			);
			target.style.setProperty(
				"--mouse-y",
				`${y}px`
			);

			// Print the CSS variables
			printMouseCoordinates(target);
		};

		const printMouseCoordinates = (element) => {
			const mouseX =
				getComputedStyle(
					element
				).getPropertyValue("--mouse-x");
			const mouseY =
				getComputedStyle(
					element
				).getPropertyValue("--mouse-y");
			console.log(
				`--mouse-x: ${mouseX}, --mouse-y: ${mouseY}`
			);
		};

		for (const lb of document.querySelectorAll(
			".lb"
		)) {
			lb.onmousemove = (e) => handleMouseMove(e);
		}
	}
);
