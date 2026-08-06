const cookies = window.TNAFrontendCookies;

if (cookies) {
  const $successMessage = document.getElementById("cookie-settings-success");
  const $form = document.getElementById("cookie-settings");
  if ($form && $successMessage) {
    $form.addEventListener("submit", (event) => {
      event.preventDefault();
      const formData = new FormData($form);
      cookies.setPreference("usage", formData.get("usage") === "true");
      cookies.setPreference("settings", formData.get("settings") === "true");
      cookies.setPreference("marketing", formData.get("marketing") === "true");
      cookies.set("cookie_preferences_set", true);
      $successMessage.removeAttribute("hidden");
      $successMessage.setAttribute("tabindex", "0");
      $successMessage.focus();
      document
        .querySelector('[data-module="tna-cookie-banner"]')
        ?.setAttribute("hidden", true);
    });
  }
  if ($successMessage) {
    $successMessage.addEventListener("blur", () => {
      $successMessage.setAttribute("tabindex", "-1");
    });
  }
}
