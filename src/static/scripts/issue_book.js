const issue_book = () => {

    const form = document.querySelector("#Form")
    const book_id = form.book_id.value
    const user_name = form.user_name.value
    const book_name = form.book_name.value
    const book_author = form.book_author.value

    if (!book_id || !user_name || !book_name || !book_author) {
        notify("All the fields are required")
        return
    }

    const formData = new FormData(form)
    formData.append("book_id", book_id)
    fetch("http://localhost:5000/books/issue", {
        method: "POST",
        body: formData
    }).then(async (response) => {
        if (response.ok) {
            location.href = "http://localhost:5000/books/issue"
        }
    })
}
