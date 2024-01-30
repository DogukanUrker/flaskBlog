/**
 *
 * @param {string} input
 */
function searchBar() {
  const input = document.querySelector("#searchBarInput").value;
  if (input === "" || input.trim() === "") {
    // do litteraly nothing
  } else {
    window.location.href = `/search/${encodeURIComponent(
      escape(input.trim())
    )}`;
  }
}
