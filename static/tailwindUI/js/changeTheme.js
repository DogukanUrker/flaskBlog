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
    "text-neutral-100 bg-neutral-900 selection:bg-neutral-800 selection:text-rose-500";
  changeTheme.innerHTML = '<i class="ti ti-moon"></i>';
  changeTheme.setAttribute("onclick", "javascript: toDark();");
}

function toDark() {
  localStorage.setItem(theme, "dark");
  body.className =
    "text-neutral-900 bg-neutral-100 selection:bg-neutral-200 selection:text-rose-500";
  changeTheme.innerHTML = '<i class="ti ti-sun"></i>';
  changeTheme.setAttribute("onclick", "javascript: toLight();");
}
