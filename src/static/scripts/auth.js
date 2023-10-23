const login = (register) => {
    const form = document.querySelector("#Form")
    const username = form.userName.value
    const password = form.password.value

    if (!username || !password) {
        notify("All the fields are required")
        return
    }

    let url;
    if (register) {
        url = "http://localhost:5000/auth/register"
        const confirmPassword = form.confirmPassword.value
        if (password.trim() !== confirmPassword.trim()) {
            notify("Passwords don't match")
            return
        }
    } else {
        url = "http://localhost:5000/auth/login"
    }

    const formData = new FormData(form)
    fetch(url, {
        method: "POST",
        body: formData,
    }).then((response) => {
        if (response.ok) {
            window.location.href = response.url
        }
    })

}
