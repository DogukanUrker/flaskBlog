function search() {
    var input = document.getElementById("searchInput").value;
    if (input === "" || input.replace(/\s/g, "") === "") {
    } else {
        window.location.href = `/search/${input.replace(/\s/g, "+")}`;
    }
}
