var root = document.querySelector(":root");
var rootStyles = getComputedStyle(root);
var btnLight = document.querySelector(".toLight");
var btnDark = document.querySelector(".toDark");

theme = "light";

if (localStorage.getItem(theme) === "light") {
  root.style.setProperty("--dark", "#000");
  root.style.setProperty("--light", "#fff");
  btnDark.style.display = "inline-block";
  btnLight.style.display = "none";
} else if (localStorage.getItem(theme) === "dark") {
  root.style.setProperty("--dark", "#fff");
  root.style.setProperty("--light", "#000");
  btnLight.style.display = "inline-block";
  btnDark.style.display = "none";
}

function toLight() {
  localStorage.setItem(theme, "light");
  root.style.setProperty("--dark", "#000");
  root.style.setProperty("--light", "#fff");
  btnLight.style.display = "none";
  btnDark.innerHTML = "🌚";
  btnDark.style.display = "inline-block";
}

function toDark() {
  localStorage.setItem(theme, "dark");
  root.style.setProperty("--dark", "#fff");
  root.style.setProperty("--light", "#000");
  btnDark.style.display = "none";
  btnLight.innerHTML = "☀️";
  btnLight.style.display = "inline-block";
}
