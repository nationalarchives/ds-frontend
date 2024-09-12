import {
  initAll,
  Cookies,
} from "@nationalarchives/frontend/nationalarchives/all.mjs";

// Set the cookies domain and extra policies even when the cookie banner is not shown
const cookiesDomain =
  document.documentElement.getAttribute("data-cookiesdomain");
const cookies = new Cookies({
  domain: cookiesDomain,
  extraPolicies: ["marketing"],
});

// if ("serviceWorker" in navigator) {
//   navigator.serviceWorker.register("/service-worker.min.js");
// }

initAll();

const initNotifications = () =>
  document
    .querySelectorAll(
      ".etna-global-alert:has(.etna-global-alert__dismiss[value][hidden])",
    )
    .forEach(($globalAlert) => {
      const $alertDismissButton = $globalAlert.querySelector(
        ".etna-global-alert__dismiss",
      );
      $alertDismissButton.hidden = false;
      $alertDismissButton.addEventListener("click", (e) => {
        const dismissedNotifications = JSON.parse(
          cookies.get("dismissed_notifications") || "[]",
        );
        const dismissedNotificationsSet = new Set(dismissedNotifications);
        dismissedNotificationsSet.add(parseInt(e.target.value));
        cookies.set(
          "dismissed_notifications",
          JSON.stringify(Array.from(dismissedNotificationsSet)),
          { session: true },
        );
        const $globalAlertWrapper = $globalAlert.closest(
          ".etna-global-alert-wrapper",
        );
        $globalAlert.remove();
        if (
          !$globalAlertWrapper.querySelector(
            ".etna-global-alert, .etna-mourning-notice",
          )
        ) {
          $globalAlertWrapper.remove();
        }
      });
    });

if (cookies.isPolicyAccepted("settings")) {
  initNotifications();
} else {
  cookies.once("changePolicy", (policies) => {
    if (policies["settings"]) {
      initNotifications();
    }
  });
}

const checkTableForScroll = ($tableWrapper) => {
  const scrollable = $tableWrapper.scrollWidth > $tableWrapper.clientWidth;
  const $tableCaption = $tableWrapper.querySelector(".tna-table__caption");
  if (scrollable) {
    $tableWrapper.setAttribute("tabindex", "0");
    $tableCaption?.classList.add("tna-table__caption--scroll");
  } else {
    $tableWrapper.removeAttribute("tabindex");
    $tableCaption?.classList.remove("tna-table__caption--scroll");
  }
};

const $tableWrappers = document.querySelectorAll(
  ".tna-table-wrapper:has(.tna-table__caption)",
);
$tableWrappers.forEach(($tableWrapper) => checkTableForScroll($tableWrapper));
window.addEventListener("resize", () => {
  $tableWrappers.forEach(($tableWrapper) => checkTableForScroll($tableWrapper));
});

document
  .querySelectorAll('a[href^="mailto:"] + .etna-email__button')
  .forEach(($emailButton) => {
    $emailButton.removeAttribute("hidden");
    $emailButton.addEventListener("click", async () => {
      try {
        await navigator.clipboard.writeText(
          $emailButton.previousElementSibling
            .getAttribute("href")
            .replace(/^mailto:/, ""),
        );
      } catch (err) {
        console.error("Failed to copy: ", err);
      }
      $emailButton.innerText = "Copied";
    });
    $emailButton.addEventListener("blur", () => {
      $emailButton.innerText = "Copy";
    });
  });
