const login = () => {
    const form = document.querySelector("form")
    const username = form.username.value
    const password = form.password.value

    if (!username || !password) {
        console.log("All the fields are required")
        return
    }

    const formData = new FormData(form)
    fetch("http://localhost:5000/auth/login", {
        method: "POST",
        body: formData,
    }).then((response) => {
        if (response.ok) {
            window.location.href = response.url
        }
    })

}
