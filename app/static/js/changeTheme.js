var body = document.querySelector("#body");
var changeTheme = document.querySelector(".changeTheme");

var theme;

if (localStorage.getItem("theme") === "dark") {
  toDark();
} else if (localStorage.getItem("theme") === "light") {
  toLight();
} else if (localStorage.getItem("theme") === null) {
  toLight();
}

function toLight() {
  "use strict";

  localStorage.setItem("theme", "light");

  document.body.className =
    "text-[#0B0104] bg-rose-50/25 selection:bg-rose-100 selection:text-rose-500";

  document.querySelector(".changeTheme").innerHTML =
    '<i class="ti ti-sun"></i>';

  document
    .querySelector('meta[name="theme-color"]')
    .setAttribute("content", "#FFFBFB");

  document
    .querySelector(".changeTheme")
    .setAttribute("onclick", "javascript: toDark();");
}

function toDark() {
  "use strict";

  localStorage.setItem("theme", "dark");

  document.body.className =
    "text-[#FFFBFB] bg-neutral-900 selection:bg-rose-950/25 selection:text-rose-500";

  document.querySelector(".changeTheme").innerHTML =
    '<i class="ti ti-moon"></i>';

  document
    .querySelector('meta[name="theme-color"]')
    .setAttribute("content", "#171717");

  document
    .querySelector(".changeTheme")
    .setAttribute("onclick", "javascript: toLight();");
}
