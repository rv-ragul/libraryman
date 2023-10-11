const importBooks = () => {
    const title = document.getElementById("title").value
    const authors = document.getElementById("authors").value
    const isbn = document.getElementById("isbn").value
    const publisher = document.getElementById("publisher").value
    const page = document.getElementById("page").value

    if (!title || !authors || !isbn || !publisher || !page) {
        console.log("All the fields are required")
        return
    }

    const form = new FormData()
    form.append("title", title)
    form.append("authors", authors)
    form.append("isbn", isbn)
    form.append("publisher", publisher)
    form.append("page", page)

    fetch("http://localhost:5000/books/import", {
        method: "POST",
        body: form
    }).then((response) => {
        console.log(response)
    })
}
