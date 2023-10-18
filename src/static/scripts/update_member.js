const notify = (msg) => {
    console.log(msg)
}

const update_member = () => {
    const form = document.querySelector("form")
    const id = form.id.value
    const name = form.name.value
    const phone = form.phone.value
    const address = form.address.value

    if (!id || !name || !phone || !address) {
        notify("All the fields are required")
        return
    }
    const formData = new FormData(form)
    formData.append("id", id)
    fetch("http://localhost:5000/members/update", {
        method: "POST",
        body: formData
    }).then(async (response) => {
        if (response.ok) {
            location.href = "http://localhost:5000/members/update"
        }
    })
}
