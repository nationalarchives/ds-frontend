const cookies = window.TNAFrontendCookies;
if (cookies) {
  const $form = document.getElementById("cookie-settings");
  const $successMessage = document.getElementById("cookie-settings-success");
  if ($form && $successMessage) {
    $form.addEventListener("submit", (e) => {
      e.preventDefault();
      const formData = new FormData($form);
      cookies.setPolicy("usage", formData.get("usage") === "true");
      cookies.setPolicy("settings", formData.get("settings") === "true");
      cookies.setPolicy("marketing", formData.get("marketing") === "true");
      cookies.set("cookie_preferences_set", true);
      $successMessage.removeAttribute("hidden");
      $successMessage.setAttribute("tabindex", "0");
      $successMessage.focus();
      document
        .querySelector('[data-module="tna-cookie-banner"]')
        ?.setAttribute("hidden", true);
    });
    $successMessage.addEventListener("blur", () => {
      $successMessage.setAttribute("tabindex", "-1");
    });
  }
}
