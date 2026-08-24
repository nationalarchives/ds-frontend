import Cookies from "@nationalarchives/cookies";

const cookies = new Cookies();

if (cookies) {
  const $successMessage = document.getElementById("cookie-settings-success");
  const $form = document.getElementById("cookie-settings");
  if ($form && $successMessage) {
    const setCookiePreferences = (formData) => {
      cookies.setPreference("usage", formData.get("usage") === "true");
      cookies.setPreference("settings", formData.get("settings") === "true");
      cookies.setPreference("marketing", formData.get("marketing") === "true");
      cookies.set("cookie_preferences_set", true);
      $successMessage.removeAttribute("hidden");
      $successMessage.setAttribute("tabindex", "0");
      $successMessage.focus();
      // document
      //   .querySelector('[data-module="tna-cookie-banner"]')
      //   ?.setAttribute("hidden", true);

      // These set cookies for backwards compatibility with the old cookie banner
      /* eslint-disable-next-line no-warning-comments */
      // TODO: Remove once the old cookie banner is no longer in use
      cookies.set("cookies_policy", JSON.stringify(cookies.preferences));
      cookies.set("dontShowCookieNotice", true);
    };
    $form.addEventListener("submit", (event) => {
      event.preventDefault();
      const formData = new FormData($form);
      setCookiePreferences(formData);
    });
  }
  if ($successMessage) {
    $successMessage.addEventListener("blur", () => {
      $successMessage.setAttribute("tabindex", "-1");
    });
  }
}
