const notify = (msg, status) => {

    const element = document.querySelector("#notification")
    element.style.display = "none";
    const msgElement = element.querySelector("#message")
    msgElement.textContent = msg
    let bgColor;
    switch (status) {
        case "info":
            bgColor = "#93e7fb"
            msgElement.style.color = "black"
            break
        case "error":
            bgColor = "#f95959";
            break;
        case "warn":
            bgColor = "#efd7bb";
            break;
        case "success":
            bgColor = "#81cfd1"
            break
        default:
            bgColor = "#efd7bb";

    }
    msgElement.style.cssText += `background-color:${bgColor}`
    element.style.display = "flex";
    setTimeout(() => {
        element.style.display = "none";
    }, 5000)
}

let dropdownVisible = false

const toggleDropdown = () => {
    const dropdown = document.querySelector("#dropdown")
    if (dropdownVisible) {
        dropdown.style.display = "none"
    }
    else {
        dropdown.style.display = "block"
    }
    dropdownVisible = !dropdownVisible
}

const showPasswordForm = () => {
    toggleDropdown()
    const updateSection = document.querySelector("#update")
    updateSection.style.display = "flex"
}

const cancelUpdate = () => {
    const updateSection = document.querySelector("#update")
    updateSection.style.display = "none"
}

const changePassword = () => {
    const form = document.querySelector("#updatePassword")
    const password = form.password.value
    const confirmPassword = form.confirmPassword.value

    if (password == "" || confirmPassword == "") {
        notify("All the fields are required!", "warn")
        return
    }
    if (password != confirmPassword) {
        notify("Passwords don't match", "error")
        return
    }

    const formData = new FormData()
    formData.append("password", password)
    fetch("http://localhost:5000/auth/update", {
        method: "POST",
        body: formData,
    }).then(async (response) => {
        if (response.ok) {
            notify("Password updated successfully!", "success")
            form.reset()
            cancelUpdate()
        } else {
            notify(await response.text(), "error")
        }
    })
}

document.addEventListener("keydown", (event) => {
    if (event.key == "Escape") {
        cancelUpdate()
    }
})

