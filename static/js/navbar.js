function search() {
    var input = document.getElementById("searchInput").value;
    if (input === "" || input.replace(/\s/g, "") === "") {
    } else {
        window.location.href = `/search/${input.replace(/\s/g, "+")}`;
    }
}
function hamburger() {
    document.getElementById("hamburgerDropdown").classList.toggle("show");
}

window.onclick = function (event) {
    if (!event.target.matches('.hamburgerBtn')) {
        var dropdowns = document.getElementsByClassName("hamburgerContent");
        var i;
        for (i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
}