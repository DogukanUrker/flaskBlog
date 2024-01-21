/**
 * Toggles the visibility of the hamburger dropdown menu
 * @param {Event} event - The click event that triggered the function
 */
function hamburger(event) {
  /**
   * The element that contains the hamburger dropdown menu
   * @type {HTMLElement}
   */
  const hamburgerDropdown = document.getElementById("hamburgerDropdown");

  /**
   * Toggles the class "show" on the hamburger dropdown menu
   */
  hamburgerDropdown.classList.toggle("show");
}

/**
 * Redirects the user to the search results page when the search button is clicked
 */
function search() {
  /**
   * The input element for the search query
   * @type {HTMLInputElement}
   */
  const input = document.querySelector("#searchInput");

  /**
   * The value of the search query
   * @type {string}
   */
  const inputValue = input.value;

  /**
   * The URL for the search results page
   * @type {string}
   */
  const searchUrl = `/search/${encodeURIComponent(escape(inputValue))}`;

  if (inputValue === "" || inputValue.trim() === "") {
    // do nothing
  } else {
    window.location.href = searchUrl;
  }
}

/**
 * Closes the hamburger dropdown menu when a click event occurs outside of the menu
 * @param {Event} event - The click event that triggered the function
 */
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
