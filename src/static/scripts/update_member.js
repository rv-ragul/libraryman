const form = document.querySelector("#Form")
const id = form.querySelector("[name=id]")
const memberName = form.querySelector("[name=name]")
const phone = form.querySelector("[name=phone]")
const address = form.querySelector("[name=address]")

const update_member = () => {

    if (!id.value || !memberName.value || !phone.value || !address.value) {
        notify("All the fields are required", "warn")
        return
    }
    const formData = new FormData(form)
    formData.append("id", id.value)
    fetch("http://localhost:5000/members/update", {
        method: "POST",
        body: formData
    }).then(async (response) => {
        if (response.ok) {
            notify("Member updated successfully!", "success")
            setTimeout(() => {
                location.search = ""
            }, 2000)
        }
    })
}

id.addEventListener("focusout", () => {
    fetch("http://localhost:5000/members/" + id.value).then(async (response) => {
        if (response.ok) {
            const res = await response.json()
            memberName.value = res.name
            phone.value = res.phone
            address.value = res.address
        } else {
            notify(await response.text(), "error")
            memberName.value = ""
            phone.value = ""
            address.value = ""
        }

    })
})
