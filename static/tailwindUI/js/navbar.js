/**
 *
 * @param {string} input
 */
function search() {
  const input = document.querySelector("#searchInput").value;
  if (input === "" || input.trim() === "") {
    // do litteraly nothing
  } else {
    window.location.href = `/search/${encodeURIComponent(
      escape(input.trim())
    )}`;
  }
}
