const importBooks = () => {
    const submitBtn = document.querySelector("#submit")
    submitBtn.disabled = true
    const form = document.querySelector("#Form")
    const formData = new FormData(form)

    fetch("http://localhost:5000/books/import", {
        method: "POST",
        body: formData
    }).then(async (response) => {
        if (response.ok) {
            const numBooks = await response.text()
            if (numBooks == 0) {
                notify(`Oops!, No books found for given criteria`, "warn")
            } else {
                notify(`Imported ${numBooks} books successfully!`, "success")
            }
        } else {
            notify(await response.text(), "error")
        }
        submitBtn.disabled = false
    })
}
