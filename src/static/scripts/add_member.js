const form = document.querySelector("#Form")
const memberName = form.querySelector("[name=name]")
const phone = form.querySelector("[name=phone]")
const address = form.querySelector("[name=address]")

const add_member = () => {
    if (!memberName.value || !phone.value || !address.value) {
        notify("All the fields are required", "error")
        return
    }

    if (String(phone.value).length != 10) {
        notify("Phone number doesn't have 10 digits", "error")
        return
    }

    const submitBtn = document.querySelector("#submit")
    submitBtn.disabled = true
    const formData = new FormData(form)
    fetch("http://localhost:5000/members/add", {
        method: "POST",
        body: formData,
    }).then(async (response) => {
        if (response.ok) {
            notify("New member added successfully!", "success")
            form.reset()
        } else {
            notify(await response.text(), "error")
        }
        submitBtn.disabled = false
    })
}
