const login = () => {
    const username = document.getElementById("username").value
    const password = document.getElementById("password").value

    if (!username || !password) {
        console.log("All the fields are required")
        return
    }

    const form = new FormData()
    form.append("username", username)
    form.append("password", password)

    fetch("http://localhost:5000/auth/login", {
        method: "POST",
        body: body,
    }).then((response) => {
        if (response.ok) {
            window.location.href = response.url
        }
    })

}
