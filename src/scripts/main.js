import {
  initAll,
  Cookies,
} from "@nationalarchives/frontend/nationalarchives/all.mjs";

const cookiesDomain =
  document.documentElement.getAttribute("data-cookiesdomain");
if (cookiesDomain) {
  new Cookies({ domain: cookiesDomain });
}

if ("serviceWorker" in navigator) {
  navigator.serviceWorker.register("/service-worker.min.js");
}

initAll();
