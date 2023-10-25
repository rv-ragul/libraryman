const return_book = (id) => {
    location.href = "http://localhost:5000/books/return?id=" + id
}

// Search books based on title and authors
const form = document.querySelector("#Form")
const title_input = form.querySelector("[name=title]");
const memberid_input = form.querySelector("[name=memberID]")
const btnSearch = form.querySelector("#search")
const btnReset = form.querySelector("#reset")

const get_books = () => {
    const url = "http://localhost:5000/books/issued"
    const params = new URLSearchParams()

    const title = title_input.value;
    const memberID = memberid_input.value;
    if (title !== '') {
        params.append("title", title)
    }
    if (memberID !== '') {
        params.append("authors", memberID)
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

memberid_input.addEventListener("keydown", (event) => {
    if (event.key == "Enter") {
        get_books()
    }
})

btnSearch.addEventListener("click", () => {
    get_books()
})

btnReset.addEventListener("click", () => {
    location.search = ""
})
