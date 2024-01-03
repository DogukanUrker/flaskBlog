var body = document.querySelector("#body");
var changeTheme = document.querySelector(".changeTheme");

var theme;

if (localStorage.getItem(theme) === "dark") {
  toDark();
} else if (localStorage.getItem(theme) === "light") {
  toLight();
}

function toLight() {
  localStorage.setItem(theme, "light");
  body.className =
    "text-neutral-100 bg-neutral-900 selection:bg-rose-500 duration-150";
  changeTheme.innerHTML = "🌞";
  changeTheme.setAttribute("onclick", "javascript: toDark();");
}

function toDark() {
  localStorage.setItem(theme, "dark");
  body.className =
    "text-neutral-900 bg-neutral-100 selection:bg-rose-500 duration-150";
  changeTheme.innerHTML = "🌚";
  changeTheme.setAttribute("onclick", "javascript: toLight();");
}
