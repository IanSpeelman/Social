document.addEventListener("DOMContentLoaded", () => {
	editButtons = document.querySelectorAll(".edit");

	for (btn of editButtons) {
		btn.addEventListener("click", (e) => {
			let postId = e.target.parentElement.dataset.post;
			// let editform = document.querySelector(".editform");
			let p = document.querySelector(`p[data-post='${postId}']`);
			let editform = p.nextElementSibling?p.nextElementSibling:false;
			// console.log(test);
			if (editform || editform.classList?.contains("hidden")) {
				editform.classList.toggle("hidden");
				p.classList.toggle("hidden");
			} else {
				p = document.querySelector(`p[data-post='${postId}']`);
				let content = p.innerText;
				let parent = p.parentElement;
				p.classList.toggle("hidden");
				let txtarea = document.createElement("textarea");
				txtarea.innerText = content;
				txtarea.setAttribute("name", "content");
				let btn = document.createElement("button");
				btn.innerText = "Edit";
				let div = document.createElement("div");
				div.append(txtarea);
				div.append(btn);
				div.setAttribute("class", "editform");
				parent.append(div);
			}
		});
	}
});
