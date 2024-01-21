/**
 * Selects the root element of the document.
 * @returns {Element} The root element of the document.
 */
function selectDocumentRoot() {
  return document.querySelector(":root");
}

/**
 * Selects the element with the given class name.
 * @param {string} className The class name of the element to select.
 * @returns {Element} The element with the given class name, or null if no element is found.
 */
function selectElementByClassName(className) {
  return document.querySelector(`.${className}`);
}

/**
 * The current theme of the application.
 * @type {string}
 */
let theme;

/**
 * Initializes the theme based on the value stored in local storage.
 */
function initTheme() {
  if (localStorage.getItem("theme") === "dark") {
    toDark();
  } else if (localStorage.getItem("theme") === "light") {
    toLight();
  } else if (localStorage.getItem("theme") === null) {
    toDark();
  }
}

/**
 * Changes the theme to light mode.
 */
function toLight() {
  // set the theme in local storage
  localStorage.setItem("theme", "light");

  // set the CSS variables
  selectDocumentRoot().style.setProperty("--themePrimary", "#000");
  selectDocumentRoot().style.setProperty("--themeSecondary", "#fff");
  selectDocumentRoot().style.setProperty("--themeHelper", "#303030");

  // update the theme button
  selectElementByClassName("changeTheme").innerHTML =
    '<i class="ti ti-sun"></i>';
  selectElementByClassName("changeTheme").setAttribute(
    "onclick",
    "javascript: toDark();"
  );
}

/**
 * Changes the theme to dark mode.
 */
function toDark() {
  // set the theme in local storage
  localStorage.setItem("theme", "dark");

  // set the CSS variables
  selectDocumentRoot().style.setProperty("--themePrimary", "#fff");
  selectDocumentRoot().style.setProperty("--themeSecondary", "#000");
  selectDocumentRoot().style.setProperty("--themeHelper", "#C6C6C6");

  // update the theme button
  selectElementByClassName("changeTheme").innerHTML =
    '<i class="ti ti-moon"></i>';
  selectElementByClassName("changeTheme").setAttribute(
    "onclick",
    "javascript: toLight();"
  );
}

initTheme();
