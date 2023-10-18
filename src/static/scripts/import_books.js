const notify = (msg) => {
    console.log(msg)
}

const importBooks = () => {
    const form = document.querySelector("form")
    const formData = new FormData(form)

    fetch("http://localhost:5000/books/import", {
        method: "POST",
        body: formData
    }).then((response) => {
        notify(response)
    })
}
