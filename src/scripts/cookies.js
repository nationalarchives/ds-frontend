// TODO: Re-enable in one year (2027-06) when all cookies should have the httpOnly flag removed

// const cookies = window.TNAFrontendCookies;

// if (cookies) {
//   const $successMessage = document.getElementById("cookie-settings-success");
//   const $form = document.getElementById("cookie-settings");
//   if ($form && $successMessage) {
//     $form.addEventListener("submit", (event) => {
//       event.preventDefault();
//       const formData = new FormData($form);
//       cookies.setPolicy("usage", formData.get("usage") === "true");
//       cookies.setPolicy("settings", formData.get("settings") === "true");
//       cookies.setPolicy("marketing", formData.get("marketing") === "true");
//       cookies.set("cookie_preferences_set", true);
//       $successMessage.removeAttribute("hidden");
//       $successMessage.setAttribute("tabindex", "0");
//       $successMessage.focus();
//       document
//         .querySelector('[data-module="tna-cookie-banner"]')
//         ?.setAttribute("hidden", true);
//     });
//   }
//   if ($successMessage) {
//     $successMessage.addEventListener("blur", () => {
//       $successMessage.setAttribute("tabindex", "-1");
//     });
//   }
// }
