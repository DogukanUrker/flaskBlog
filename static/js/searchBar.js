function searchBar() {
    var input = document.querySelector("#searchBarInput").value;
    console.log(input)
    if (input === "" || input.replace(/\s/g, "") === "") {
    } else {
        window.location.href = `/search/${input.replace(/\s/g, "+")}`;
    }
}