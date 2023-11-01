const return_book = () => {
    const form = document.querySelector("#Form")
    const bookID = form.bookID.value
    const memberID = form.memberID.value
    const _returnDate = form.returnDate.value
    const paid = form.querySelector("[name=paid]")

    if (!bookID || !memberID || !_returnDate) {
        notify("All fields are required", "warn")
        return
    }

    const formData = new FormData()
    let returnDate = new Date(_returnDate)
    formData.append("bookID", bookID)
    formData.append("memberID", memberID)
    formData.append("returnDate", returnDate.toUTCString())
    if (paid.checked) {
        formData.append("paid", "true")
    }
    fetch("http://localhost:5000/books/return", {
        method: "POST",
        body: formData
    }).then((response) => {
        if (response.ok) {
            location.search = ""
        }
    })
}
