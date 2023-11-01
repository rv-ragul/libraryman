const remove_member = (id) => {
    fetch("http://localhost:5000/members/" + id, {
        method: "DELETE"
    }).then((response) => {
        if (response.ok) {
            const member = document.getElementById(id)
            member.parentNode.removeChild(member)
            notify("Member removed successfully", "success")
        }
        else {
            notify(response.text, "error")
        }

    })
}

const update_member = (id) => {
    location.href = "http://localhost:5000/members/update?id=" + id
}

// Search members based on id or name
const form = document.querySelector("#Form")
const id_input = form.querySelector("[name=id]")
const name_input = form.querySelector("[name=name]")
const btnSearch = form.querySelector("#search")
const btnReset = form.querySelector("#reset")

id_input.addEventListener("input", (_event) => {
    name_input.value = ''
})

name_input.addEventListener("input", (_event) => {
    id_input.value = ''
})

const get_members = () => {
    const url = "http://localhost:5000/members/";
    const params = new URLSearchParams()

    const memberID = id_input.value;
    const memberName = name_input.value;
    if (memberID !== '') {
        params.append("id", memberID)

    } else if (memberName !== '') {
        params.append("name", memberName)
    }
    if (params.size) {
        location.href = url + "?" + params.toString();
    }
}

id_input.addEventListener("keydown", (event) => {
    if (event.key == "Enter") {
        get_members()
    }
})

name_input.addEventListener("keydown", (event) => {
    if (event.key == "Enter") {
        get_members()
    }
})

btnSearch.addEventListener("click", () => {
    get_members()
})

btnReset.addEventListener("click", () => {
    location.search = ""
})
