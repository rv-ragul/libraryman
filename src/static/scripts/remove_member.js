const remove_member = (id) => {
    fetch("http://localhost:5000/members/" + id, {
        method: "DELETE"
    }).then((response) => {
        if (response.ok) {
            const member = document.getElementById(id)
            member.parentNode.removeChild(member)
        }
    })
}

const update_member = (id) => {
    fetch("http://localhost:5000/members/" + id, {
        method: "PUT",
    }).then((response) => {
        console.log(response)
    })
}
