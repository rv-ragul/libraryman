const notify = (msg) => {
    console.log(msg)
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

const showChangeForm = () => {
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
        notify("All the fields are required!")
        return
    }
    if (password != confirmPassword) {
        notify("Passwords don't match")
        return
    }

    const formData = new FormData()
    formData.append("password", password)
    fetch("http://localhost:5000/auth/update", {
        method: "POST",
        body: formData,
    }).then((response) => {
        if (response.ok) {
            notify("Password updated successfully!")
            form.reset()
            cancelUpdate()
        }
    })
}

document.addEventListener("keydown", (event) => {
    if (event.key == "Escape") {
        cancelUpdate()
    }
})

