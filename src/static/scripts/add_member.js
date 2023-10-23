const add_member = () => {
    const form = document.querySelector("#Form")
    const name = form.name.value
    const phone = form.phone.value
    const address = form.address.value

    if (!name || !phone || !address) {
        notify("All the fields are required")
        return
    }

    const formData = new FormData(form)
    fetch("http://localhost:5000/members/add", {
        method: "POST",
        body: formData,
    }).then((response) => {
        if (response.ok) {
            notify("New member added successfully!")
            form.reset()
        }
    })
}
