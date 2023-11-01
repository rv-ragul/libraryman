const issue_book = () => {

    const form = document.querySelector("#Form")
    const bookID = form.bookID.value
    const memberID = form.memberID.value
    const title = form.title.value
    const authors = form.authors.value

    if (!bookID || !memberID || !title || !authors) {
        notify("All the fields are required", "warn")
        return
    }

    const formData = new FormData(form)
    formData.append("bookID", bookID)
    fetch("http://localhost:5000/books/issue", {
        method: "POST",
        body: formData
    }).then(async (response) => {
        if (response.ok) {
            notify("Book issued successfully!", "success")
            setTimeout(() => {
                location.search = ""
            }, 3000)
        }
    })
}
