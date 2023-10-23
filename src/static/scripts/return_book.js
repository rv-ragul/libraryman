const return_book = () => {
    const form = document.querySelector("#Form")
    const bookID = form.bookID.value
    const _returnDate = form.returnDate.value

    if (!bookID || !_returnDate) {
        notify("All fields are required")
        return
    }

    const formData = new FormData(form)
    let returnDate = new Date(_returnDate)
    formData.set("return_date", returnDate.toUTCString())
    fetch("http://localhost:5000/books/return", {
        method: "POST",
        body: formData
    }).then((response) => {
        notify(response)
        if (response.ok) {
            form.reset()
        }
    })
}
