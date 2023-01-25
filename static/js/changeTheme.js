var root = document.querySelector(":root");
var changeTheme = document.querySelector(".changeTheme");

theme = "dark";

if (localStorage.getItem(theme) === "dark") {
  toDark()
}
else if (localStorage.getItem(theme) === "light") {
  toLight()
}

function toLight() {
  localStorage.setItem(theme, "light");
  root.style.setProperty("--dark", "#000");
  root.style.setProperty("--light", "#fff");
  root.style.setProperty("--jet", "#303030");
  changeTheme.innerHTML = "🌚";
  changeTheme.setAttribute("onclick", "javascript: toDark();")
}

function toDark() {
  localStorage.setItem(theme, "dark");
  root.style.setProperty("--dark", "#fff");
  root.style.setProperty("--light", "#000");
  root.style.setProperty("--jet", "#C6C6C6")
  changeTheme.innerHTML = "🌞";
  changeTheme.setAttribute("onclick", "javascript: toLight();")
}
