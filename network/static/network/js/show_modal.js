document.addEventListener("DOMContentLoaded", () => { 
    const modal = document.querySelector(".post-create-modal")
    const button = document.querySelector(".modal-show-button")

    button.addEventListener("click", () => {
        modal.classList.toggle("hidden")
    })
})