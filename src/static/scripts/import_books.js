const importBooks = () => {
    const form = document.querySelector("#Form")
    const formData = new FormData(form)

    fetch("http://localhost:5000/books/import", {
        method: "POST",
        body: formData
    }).then((response) => {
        if (response.ok) {
            notify("Books imported successfully!", "success")
        } else {
            notify(response.text, "error")
        }
    })
}
