const notify = (msg) => {
    console.log(msg)
}

const issue_book = () => {
    const form = document.querySelector("form")
    const book_id = form.book_id.value
    const user_name = form.user_name.value
    const book_name = form.book_name.value
    const book_author = form.book_author.value

    if (!book_id || !user_name || !book_name || !book_author) {
        notify("All the fields are required")
        return
    }

    const formData = new FormData(form)
    fetch("http://localhost:5000/books/issue", {
        method: "POST",
        body: formData
    }).then(async (response) => {
        notify(response)
        notify(await response.text())
    })
}

// Search books based on title and authors
const form = document.querySelector("form")
const title_input = form.querySelector("[name=title]");
const authors_input = form.querySelector("[name=authors]")
const btnSearch = form.querySelector("#search")
const btnReset = form.querySelector("#reset")

const get_members = () => {
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
        get_members()
    }
})

authors_input.addEventListener("keydown", (event) => {
    if (event.key == "Enter") {
        get_members()
    }
})

btnSearch.addEventListener("click", () => {
    get_members()
})

btnReset.addEventListener("click", () => {
    location.href = "http://localhost:5000/books/"
})
