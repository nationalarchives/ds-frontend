import {
  initAll,
  Cookies,
} from "@nationalarchives/frontend/nationalarchives/all.mjs";

window.VIDEOJS_NO_DYNAMIC_STYLE = true;
window.VIDEOJS_NO_AUTOMATIC_YOUTUBE_INIT = true;

// if ("serviceWorker" in navigator) {
//   navigator.serviceWorker.register("/service-worker.min.js");
// }

initAll();

const cookies = new Cookies();

const initNotifications = () => {
  const initialDismissedNotifications = JSON.parse(
    cookies.get("dismissed_notifications") || "[]",
  );
  document
    .querySelectorAll(
      ".etna-global-alert:has(.etna-global-alert__dismiss[value][hidden])",
    )
    .forEach(($globalAlert) => {
      const $alertDismissButton = $globalAlert.querySelector(
        ".etna-global-alert__dismiss",
      );
      const alertUid = parseInt($alertDismissButton.value);
      if (initialDismissedNotifications.includes(alertUid)) {
        $globalAlert.hidden = true;
      } else {
        $alertDismissButton.hidden = false;
        $alertDismissButton.addEventListener("click", () => {
          const dismissedNotifications = JSON.parse(
            cookies.get("dismissed_notifications") || "[]",
          );
          const dismissedNotificationsSet = new Set(dismissedNotifications);
          dismissedNotificationsSet.add(parseInt(alertUid));
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
      }
    });
};

if (cookies.isPolicyAccepted("settings")) {
  initNotifications();
} else {
  cookies.once("changePolicy", (policies) => {
    if (policies["settings"]) {
      initNotifications();
    }
  });
}

// document
//   .querySelectorAll('a[href^="mailto:"] + .etna-email__button')
//   .forEach(($emailButton) => {
//     const originalEmailButtonHTML = $emailButton.innerHTML;
//     $emailButton.removeAttribute("hidden");
//     $emailButton.addEventListener("click", async () => {
//       try {
//         await navigator.clipboard.writeText(
//           $emailButton.previousElementSibling
//             .getAttribute("href")
//             .replace(/^mailto:/, ""),
//         );
//       } catch (err) {
//         console.error("Failed to copy: ", err);
//       }
//       $emailButton.innerHTML = "Copied";
//     });
//     $emailButton.addEventListener("blur", () => {
//       $emailButton.innerHTML = originalEmailButtonHTML;
//     });
//   });

const apiHost = "http://localhost:8000";
fetch(`${apiHost}/userbar/`)
  .then((res) => res.text())
  .then((userbar) => {
    const $userbar = document.createElement("div");
    $userbar.id = "wagtail-userbar";
    $userbar.innerHTML = userbar;
    document.body.appendChild($userbar);
  });

const vendorScript = document.createElement("script");
vendorScript.src = `${apiHost}/wagtail-static/wagtailadmin/js/vendor.js`;
document.body.appendChild(vendorScript);
const userbarScript = document.createElement("script");
userbarScript.src = `${apiHost}/wagtail-static/wagtailadmin/js/userbar.js`;
document.body.appendChild(userbarScript);
