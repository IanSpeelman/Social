document.addEventListener("DOMContentLoaded", () => {
	posts = document.querySelectorAll(".post");
	// posts[0].children[2].children[0].dataset.postId  post id
	// posts[0].children[2].children[0] event listener

	for (post of posts) {
		post.children[2].children[0].addEventListener(
			"click",
			(e) => {
				const postId = e.target.parentElement.dataset.post;
				const url = `/post/${postId}/like`;
				fetch(url).then(() => {
					if (
						e.target.parentElement.children[1].classList.contains(
							"hidden",
						)
					) {
						currentvalue =
							e.target.parentElement.parentElement.children[1]
								.innerText;
						currentvalue++;
						e.target.parentElement.parentElement.children[1].innerText = `${currentvalue}`;

					} else {
						currentvalue =
							e.target.parentElement.parentElement.children[1]
								.innerText;
						currentvalue--;
						e.target.parentElement.parentElement.children[1].innerText = `${currentvalue}`;
					}
					e.target.parentElement.children[0].classList.toggle(
						"hidden",
					);
					e.target.parentElement.children[1].classList.toggle(
						"hidden",
					);
				});
			},
			true,
		);
		fetch(`/post/${post.dataset.post}`)
			.then((res) => res.json())
			.then((res) => {
				currentPost = document.querySelector(
					`div.post[data-post="${res.post}"]`,
				);

				currentPost.children[2].children[1].innerText = res.likes;
				if (res.likedByUser) {
					currentPost.children[2].children[0].children[0].classList.toggle(
						"hidden",
					);
					currentPost.children[2].children[0].children[1].classList.toggle(
						"hidden",
					);
				}
			});
	}
});
