import Cookies from "@nationalarchives/cookies";

const cookies = new Cookies();

if (cookies.exists("theme")) {
  document.documentElement.classList.add(
    `tna-template--${cookies.get("theme")}-theme`,
  );
}
