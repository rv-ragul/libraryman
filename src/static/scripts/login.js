const validate = () => {
    const username = document.getElementById("username").value
    const password = document.getElementById("password").value
    let error = false
    if (!username) {
        error = true
    }
    if (!password) {
        error = true
    }
    if (!error) {
        const form = new FormData()
        form.append("username", username)
        form.append("password", password)
        return form
    }
}

const login = (body) => {
    const options = {
        method: "POST",
        body: body,
    }
    fetch("http://localhost:5000/auth/login", options)
        .then((response) => {
            if (response.ok) {
                window.location.href = response.url
            }
        })

}

const submit = () => {
    const result = validate()
    if (result) {
        login(result)
    }
}

const submitBtn = document.getElementById("submitBtn")
submitBtn.addEventListener('click', submit)
