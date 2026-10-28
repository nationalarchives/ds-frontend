import Cookies from "@nationalarchives/cookies";
import { initAll } from "@nationalarchives/frontend/nationalarchives/all.mjs";

window.VIDEOJS_NO_DYNAMIC_STYLE = true;
window.VIDEOJS_NO_AUTOMATIC_YOUTUBE_INIT = true;

// If ("serviceWorker" in navigator) {
//   Navigator.serviceWorker.register("/service-worker.min.js");
// }

initAll();

const cookies = new Cookies();
window.TNAFrontendCookies = cookies;

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
      const alertUid = parseInt($alertDismissButton.value, 10);
      if (initialDismissedNotifications.includes(alertUid)) {
        $globalAlert.hidden = true;
      } else {
        $alertDismissButton.hidden = false;
        $alertDismissButton.addEventListener("click", () => {
          const dismissedNotifications = JSON.parse(
            cookies.get("dismissed_notifications") || "[]",
          );
          const dismissedNotificationsSet = new Set(dismissedNotifications);
          dismissedNotificationsSet.add(parseInt(alertUid, 10));
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

const setTheme = (theme) => {
  if (theme === "light") {
    document.documentElement.classList.remove(
      "tna-template--dark-theme",
      "tna-template--system-theme",
    );
  } else if (theme === "dark") {
    document.documentElement.classList.remove("tna-template--system-theme");
    document.documentElement.classList.add(`tna-template--dark-theme`);
  } else {
    document.documentElement.classList.remove("tna-template--dark-theme");
    document.documentElement.classList.add(`tna-template--system-theme`);
  }
};

const updateThemeFromCookie = () => {
  if (cookies.exists("theme")) {
    setTheme(cookies.get("theme"));
  } else {
    setTheme("system");
  }
};

if (cookies.preference("settings")) {
  initNotifications();
  updateThemeFromCookie();
} else {
  cookies.once("changePreference", (policies) => {
    if (policies.settings) {
      initNotifications();
      updateThemeFromCookie();
    }
  });
}

cookies.on("changePreference", (data) => {
  if (Object.hasOwn(data, "settings")) {
    if (data.settings !== true) {
      cookies.delete("theme");
      cookies.delete("dismissed_notifications");
    }
  }
});

window.matchMedia("print").addEventListener("change", (evt) => {
  if (evt.matches) {
    document
      .querySelectorAll(
        "img[loading=lazy], iframe[loading=lazy], video[loading=lazy]",
      )
      .forEach(($element) => {
        $element.removeAttribute("loading");
      });
  }
});
