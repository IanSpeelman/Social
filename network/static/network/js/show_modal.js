document.addEventListener("DOMContentLoaded", () => { 
    const login = document.querySelector("#post-list").dataset.login
    
    if(login === "true"){
        const modal = document.querySelector(".post-create-modal")
        const button = document.querySelector(".modal-show-button")
        button.addEventListener("click", () => {
            modal.classList.toggle("hidden")
        })
    }
})