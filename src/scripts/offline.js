import Cookies from "@nationalarchives/frontend/nationalarchives/lib/cookies.mjs";

const cookies = new Cookies();
if (cookies.exists("theme")) {
  document.documentElement.classList.add(
    `tna-template--${cookies.get("theme")}-theme`,
  );
}

const $logo = document.getElementById("logo");

$logo.addEventListener("dblclick", () => {
  $logo.classList.toggle("spin");
});
