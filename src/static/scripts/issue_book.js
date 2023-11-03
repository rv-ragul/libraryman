const form = document.querySelector("#Form")
const bookID = form.querySelector("[name=bookID]")
const title = form.querySelector("[name=title]")
const authors = form.querySelector("[name=authors]")

const resetForm = () => {
    location.search = ""
}
const issue_book = () => {
    if (!bookID.value || !memberID.value) {
        notify("Please fill the required fields", "warn")
        return
    }

    const submitBtn = document.querySelector("#submit")
    submitBtn.disabled = true
    const formData = new FormData(form)
    formData.append("bookID", bookID)
    fetch("http://localhost:5000/books/issue", {
        method: "POST",
        body: formData
    }).then(async (response) => {
        if (response.ok) {
            notify("Book issued successfully!", "success")
            setTimeout(() => {
                resetForm()
            }, 2000)
        }
        else {
            notify(await response.text(), "error")
        }
        submitBtn.disabled = false
    })
}

bookID.addEventListener("focusout", () => {
    fetch("http://localhost:5000/books/" + bookID.value).then(async (response) => {
        if (response.ok) {
            const res = await response.json()
            title.value = res.title
            authors.value = res.authors
        }
        else {
            notify(await response.text(), "error")
            title.value = ""
            authors.value = ""
        }
    })
})
