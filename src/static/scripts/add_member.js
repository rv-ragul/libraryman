const add_member = () => {
    const name = document.getElementById("name").value
    const phone = document.getElementById("phone").value
    const address = document.getElementById("address").value

    if (!name || !phone || !address) {
        console.log("All the fields are required")
        return
    }

    const form = new FormData()
    form.append("name", name)
    form.append("phone", phone)
    form.append("address", address)

    fetch("http://localhost:5000/members/add", {
        method: "POST",
        body: form,
    }).then((response) => {
        if (response.ok) {
            console.log("New member added successfully!")
        }
    })
}
