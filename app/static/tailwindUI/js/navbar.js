function search() {
  const input = document.querySelector("#searchInput").value;
  if (input === "" || input.trim() === "") {
  } else {
    window.location.href = `/search/${encodeURIComponent(
      escape(input.trim()),
    )}`;
  }
}
