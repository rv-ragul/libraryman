const issue_book = (id) => {
    location.href = "http://localhost:5000/books/issue?id=" + id
}

// Search books based on title and authors
const form = document.querySelector("#Form")
const title_input = form.querySelector("[name=title]");
const authors_input = form.querySelector("[name=authors]")
const btnSearch = form.querySelector("#search")
const btnReset = form.querySelector("#reset")

const get_books = () => {
    const url = "http://localhost:5000/books/"
    const params = new URLSearchParams()

    const title = title_input.value;
    const authors = authors_input.value;
    if (title !== '') {
        params.append("title", title)
    }
    if (authors !== '') {
        params.append("authors", authors)
    }
    if (params.size) {
        location.href = url + "?" + params.toString()
    }

}

title_input.addEventListener("keydown", (event) => {
    if (event.key == "Enter") {
        get_books()
    }
})

authors_input.addEventListener("keydown", (event) => {
    if (event.key == "Enter") {
        get_books()
    }
})

btnSearch.addEventListener("click", () => {
    get_books()
})

btnReset.addEventListener("click", () => {
    location.href = "http://localhost:5000/books/"
})
