const return_book = () => {
    const form = document.querySelector("form")
    const book_id = form.book_id.value
    const return_date = form.return_date.value

    if (!book_id || !return_date) {
        console.log("All fields are required")
        return
    }

    const formData = new FormData(form)
    formData.set("return_date", new Date(return_date))
    fetch("http://localhost:5000/books/return", {
        method: "POST",
        body: formData
    }).then((response) => {
        console.log(response)
    })
}
