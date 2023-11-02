const remove_member = (id) => {
    fetch("http://localhost:5000/members/" + id, {
        method: "DELETE"
    }).then(async(response) => {
        if (response.ok) {
            const member = document.getElementById(id)
            member.parentNode.removeChild(member)
            notify("Member removed successfully", "success")
        }
        else {
            notify(await response.text(), "error")
        }

    })
}

const update_member = (id) => {
    location.href = "http://localhost:5000/members/update?id=" + id
}

// Search members based on id or name
const document = document.querySelector("#Form")
const id_input = document.querySelector("[name=id]")
const name_input = document.querySelector("[name=name]")
const btnSearch = document.querySelector("#search")
const btnReset = document.querySelector("#reset")

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
