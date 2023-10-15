const login = (register) => {
    const form = document.querySelector("form")
    const username = form.username.value
    const password = form.password.value

    if (!username || !password) {
        console.log("All the fields are required")
        return
    }

    let url;
    if (register) {
        url = "http://localhost:5000/auth/register"
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
