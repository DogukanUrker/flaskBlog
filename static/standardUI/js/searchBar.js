function searchBar() {
  const input = document.querySelector("#searchBarInput").value;
  if (input === "" || input.trim() === "") {
  } else {
    window.location.href = `/search/${encodeURIComponent(
      escape(input.trim())
    )}`;
  }
}
