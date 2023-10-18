const notify = (msg) => {
    console.log(msg)
}

const return_book = () => {
    const form = document.querySelector("form")
    const book_id = form.book_id.value
    const _return_date = form.return_date.value

    if (!book_id || !_return_date) {
        notify("All fields are required")
        return
    }

    const formData = new FormData(form)
    let return_date = new Date(_return_date)
    formData.set("return_date", return_date.toUTCString())
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
