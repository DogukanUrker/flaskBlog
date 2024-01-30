// Get the body element of the document
var body = document.querySelector("#body");
// Get the button element that changes the theme
var changeTheme = document.querySelector(".changeTheme");

// Declare a variable to store the theme
var theme;

// Check the value of the theme in the local storage
if (localStorage.getItem("theme") === "dark") {
  // If it is dark, call the toDark function
  toDark();
} else if (localStorage.getItem("theme") === "light") {
  // If it is light, call the toLight function
  toLight();
} else if (localStorage.getItem("theme") === null) {
  // If it is null, meaning the user has not set a preference, call the toLight function
  toLight();
}

/**
 * Changes the theme of the website to light mode.
 * @function
 */
function toLight() {
  "use strict";

  // Set the theme in local storage to light
  localStorage.setItem("theme", "light");

  // Update the CSS class of the body element to use light colors
  document.body.className =
    "text-[#0B0104] bg-rose-50/25 selection:bg-rose-100 selection:text-rose-500";

  // Update the HTML content of the button to show a sun icon
  document.querySelector(".changeTheme").innerHTML =
    '<i class="ti ti-sun"></i>';

  // Update the meta tag for the theme color to match the light background document
  document
    .querySelector('meta[name="theme-color"]')
    .setAttribute("content", "#FFFBFB");

  // Update the onclick event of the button to call the toDark function when clicked
  document
    .querySelector(".changeTheme")
    .setAttribute("onclick", "javascript: toDark();");
}

/**
 * Changes the theme of the website to dark mode.
 * @function
 */
function toDark() {
  "use strict";

  // Set the theme in local storage to dark
  localStorage.setItem("theme", "dark");

  // Update the CSS class of the body element to use dark colors
  document.body.className =
    "text-[#FFFBFB] bg-neutral-900 selection:bg-rose-950/25 selection:text-rose-500";

  // Update the HTML content of the button to show a moon icon
  document.querySelector(".changeTheme").innerHTML =
    '<i class="ti ti-moon"></i>';

  // Update the meta tag for the theme color to match the dark background document
  document
    .querySelector('meta[name="theme-color"]')
    .setAttribute("content", "#171717");

  // Update the onclick event of the button to call the toLight function when clicked
  document
    .querySelector(".changeTheme")
    .setAttribute("onclick", "javascript: toLight();");
}
