var root = document.querySelector(":root");
var rootStyles = getComputedStyle(root);
var changeTheme = document.querySelector(".changeTheme");

theme = "dark";

if (localStorage.getItem(theme) === "light") {
  toLight()
} else if (localStorage.getItem(theme) === "dark") {
  toDark()
}

function toLight() {
  localStorage.setItem(theme, "light");
  root.style.setProperty("--dark", "#000");
  root.style.setProperty("--light", "#fff");
  changeTheme.innerHTML = "🌚";
  changeTheme.setAttribute("onclick", "javascript: toDark();")
}

function toDark() {
  localStorage.setItem(theme, "dark");
  root.style.setProperty("--dark", "#fff");
  root.style.setProperty("--light", "#000");
  changeTheme.innerHTML = "🌞";
  changeTheme.setAttribute("onclick", "javascript: toLight();")
}
