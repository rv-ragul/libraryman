const validate = () => {
    const name = document.getElementById("name").value
    const phone = document.getElementById("phone").value
    const address = document.getElementById("address").value

    let error = false
    if (!name) {
        error = true
    }
    if (!password) {
        error = true
    }
    if (!address) {
        error = true
    }
    if (!error) {
        const form = new FormData()
        form.append("name", name)
        form.append("phone", phone)
        form.append("address", address)
        return form
    }
}

const add_member = () => {
    const result = validate()
    if (!result) return

    const options = {
        method: "POST",
        body: result,
    }

    fetch("http://localhost:5000/members/add", options)
        .then((response) => {
            if (response.ok) {

            }
        })
}
