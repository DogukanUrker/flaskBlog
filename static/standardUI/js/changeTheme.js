var root = document.querySelector(":root");
var changeTheme = document.querySelector(".changeTheme");

var theme;

if (localStorage.getItem(theme) === "dark") {
  toDark();
} else if (localStorage.getItem(theme) === "light") {
  toLight();
}

function toLight() {
  localStorage.setItem(theme, "light");
  root.style.setProperty("--themePrimary", "#000");
  root.style.setProperty("--themeSecondary", "#fff");
  root.style.setProperty("--themeHelper", "#303030");
  changeTheme.innerHTML =
    '<svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-sun" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M12 12m-4 0a4 4 0 1 0 8 0a4 4 0 1 0 -8 0" /><path d="M3 12h1m8 -9v1m8 8h1m-9 8v1m-6.4 -15.4l.7 .7m12.1 -.7l-.7 .7m0 11.4l.7 .7m-12.1 -.7l-.7 .7" /></svg>';
  changeTheme.setAttribute("onclick", "javascript: toDark();");
}

function toDark() {
  localStorage.setItem(theme, "dark");
  root.style.setProperty("--themePrimary", "#fff");
  root.style.setProperty("--themeSecondary", "#000");
  root.style.setProperty("--themeHelper", "#C6C6C6");
  changeTheme.innerHTML =
    '<svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-moon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M12 3c.132 0 .263 0 .393 0a7.5 7.5 0 0 0 7.92 12.446a9 9 0 1 1 -8.313 -12.454z" /></svg>';
  changeTheme.setAttribute("onclick", "javascript: toLight();");
}
