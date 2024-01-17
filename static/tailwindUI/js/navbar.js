function search() {
  const input = document.querySelector("#searchInput").value;
  if (input === "" || input.trim() === "") {
  } else {
    window.location.href = `/search/${encodeURIComponent(
      escape(input.trim())
    )}`;
  }
}

function hamburger() {
  document.getElementById("hamburgerDropdown").classList.toggle("show");
}

window.onclick = function(event) {
  if (!event.target.matches(".hamburgerBtn")) {
    var dropdowns = document.getElementsByClassName("hamburgerContent");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains("show")) {
        openDropdown.classList.remove("show");
      }
    }
  }
};
