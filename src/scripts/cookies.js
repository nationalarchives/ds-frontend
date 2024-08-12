const cookies = window.TNAFrontendCookies;
if (cookies) {
  const $form = document.getElementById("cookie-settings");
  const $successMessage = document.getElementById("cookie-settings-success");
  $form.addEventListener("submit", (e) => {
    e.preventDefault();
    const formData = new FormData($form);
    cookies.setPolicy("usage", formData.get("usage") === "true");
    cookies.setPolicy("settings", formData.get("settings") === "true");
    cookies.setPolicy("marketing", formData.get("marketing") === "true");
    $successMessage.removeAttribute("hidden");
    $successMessage.setAttribute("tabindex", "-1");
    $successMessage.focus();
  });
}
