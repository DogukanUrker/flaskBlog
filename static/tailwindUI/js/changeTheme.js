var body = document.querySelector("#body");
var changeTheme = document.querySelector(".changeTheme");

var theme;

if (localStorage.getItem("theme") === "dark") {
  toDark();
} else if (localStorage.getItem("theme") === "light") {
  toLight();
} else if (localStorage.getItem("theme") === null) {
  toDark();
}
/**
 * Changes the theme of the website to light mode.
 * @function
 */
function toLight() {
  "use strict";

  // Set the theme in local storage
  localStorage.setItem("theme", "light");

  // Update the CSS class of the body element
  document.body.className =
    "text-neutral-900 bg-neutral-100 selection:bg-neutral-800 selection:text-rose-500";

  // Update the HTML content of the button
  document.querySelector(".changeTheme").innerHTML =
    '<i class="ti ti-sun"></i>';

  // Update the onclick event of the button
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

  // Set the theme in local storage
  localStorage.setItem("theme", "dark");

  // Update the CSS class of the body element
  document.body.className =
    "text-neutral-100 bg-neutral-900 selection:bg-neutral-800 selection:text-rose-500";

  // Update the HTML content of the button
  document.querySelector(".changeTheme").innerHTML =
    '<i class="ti ti-moon"></i>';

  // Update the onclick event of the button
  document
    .querySelector(".changeTheme")
    .setAttribute("onclick", "javascript: toLight();");
}
