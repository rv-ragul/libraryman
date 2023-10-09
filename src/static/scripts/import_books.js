const importBooks = () => {
    const title = document.getElementById("title").value
    const authors = document.getElementById("authors").value
    const isbn = document.getElementById("isbn").value
    const publisher = document.getElementById("publisher").value
    const page = document.getElementById("page").value

    const form = new FormData()
    form.append("title", title)
    form.append("authors", authors)
    form.append("isbn", isbn)
    form.append("publisher", publisher)
    form.append("page", page)

    const options = {
        method: "POST",
        body: form
    }
    fetch("http://localhost:5000/books/import", options)
        .then((response) => {
            console.log(response)
        })
}
