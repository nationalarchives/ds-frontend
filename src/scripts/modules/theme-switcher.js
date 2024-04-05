import Cookies from "@nationalarchives/frontend/nationalarchives/lib/cookies.mjs";

const cookies = new (window.TNAFrontend?.Cookies || Cookies)();

const $themeSelector = document.getElementById("theme-selector");

const showThemeSelector = () => {
  $themeSelector.removeAttribute("hidden");
};
const hideThemeSelector = () => {
  $themeSelector.setAttribute("hidden", true);
};

const setTheme = (theme) => {
  if (theme === "light") {
    document.documentElement.classList.remove(
      "tna-template--system-theme",
      "tna-template--dark-theme",
    );
  } else if (theme === "dark") {
    document.documentElement.classList.remove("tna-template--system-theme");
    document.documentElement.classList.add(`tna-template--dark-theme`);
  } else if (theme === "system") {
    document.documentElement.classList.remove("tna-template--dark-theme");
    document.documentElement.classList.add(`tna-template--system-theme`);
  } else {
    return;
  }
  cookies.set("theme", theme);
};

const $themeSelectorButtons = $themeSelector.querySelectorAll(
  "button.etna-theme-selector[value]",
);
Array.from($themeSelectorButtons).forEach(($themeSelectorButton) => {
  $themeSelectorButton.addEventListener("click", (e) => {
    const $button = e.target;
    setTheme($button.value);
    deselectAllThemeSelectorButtons();
    selectThemeSelectorButton($button)
  });
});

const selectThemeSelectorButton = ($button) => {
  $button.classList.remove("tna-button--plain");
  $button.setAttribute("aria-current", true)
};

const deselectAllThemeSelectorButtons = () => {
  Array.from($themeSelectorButtons).forEach(($themeSelectorButton) => {
    $themeSelectorButton.classList.add("tna-button--plain");
    $themeSelectorButton.removeAttribute("aria-current")
  });
};

if (cookies.isPolicyAccepted("settings")) {
  showThemeSelector();
}
cookies.on("changePolicy", (data) => {
  if (Object.hasOwn(data, "settings")) {
    if (data.settings === true) {
      showThemeSelector();
    } else {
      cookies.delete("theme");
      hideThemeSelector();
    }
  }
});

// ++++++++++++++++++++++++++++++++++++++++++
// OLD
// ++++++++++++++++++++++++++++++++++++++++++

// const setDarkTheme = (dark = false) => {
//   document.documentElement.classList.remove("tna-template--system-theme");
//   if (dark) {
//     document.documentElement.classList.remove("tna-template--light-theme");
//     document.documentElement.classList.add(`tna-template--dark-theme`);
//   } else {
//     document.documentElement.classList.remove("tna-template--dark-theme");
//     document.documentElement.classList.add(`tna-template--light-theme`);
//   }
// };

// const setThemeFromCookie = () => {
//   setDarkTheme(
//     cookies.exists("dark_theme") && cookies.hasValue("dark_theme", "true"),
//   );
// };

// const setThemeFromUserPref = () => {
//   // Default is light
//   setDarkTheme(false);
//   // setDarkTheme(
//   //   window.matchMedia("(prefers-color-scheme: dark)")?.matches || false,
//   // );
// };

// const setThemeCookieFromUserPref = () => {
//   // Default is light
//   cookies.set("dark_theme", false);
//   // cookies.set(
//   //   "dark_theme",
//   //   window.matchMedia("(prefers-color-scheme: dark)")?.matches || false,
//   // );
// };

// const addThemeSwitcher = () => {
//   // TODO: These buttons should be in the HTML of the header with a hidden attribute which is then removed by this JS
//   if (document.getElementById("theme-switcher")) {
//     return;
//   }

//   const topNavigation = document.querySelector(
//     ".tna-global-header__top-navigation",
//   );

//   const themeButtonsWrapper = document.createElement("li");
//   themeButtonsWrapper.classList.add("tna-global-header__top-navigation-item");
//   themeButtonsWrapper.setAttribute("id", "theme-switcher");

//   const lightThemeButton = document.createElement("button");
//   lightThemeButton.classList.add(
//     "tna-global-header__top-navigation-link",
//     "tna-global-header__top-navigation-link--light",
//   );
//   lightThemeButton.innerHTML = `<i class="fa-solid fa-sun" aria-hidden="true"></i>Switch to light theme`;

//   const darkThemeButton = document.createElement("button");
//   darkThemeButton.classList.add(
//     "tna-global-header__top-navigation-link",
//     "tna-global-header__top-navigation-link--dark",
//   );
//   darkThemeButton.innerHTML = `<i class="fa-solid fa-moon" aria-hidden="true"></i>Switch to dark theme`;

//   lightThemeButton.addEventListener("click", () => {
//     cookies.set("dark_theme", false);
//     setThemeFromCookie();
//     darkThemeButton.focus();
//   });

//   darkThemeButton.addEventListener("click", () => {
//     cookies.set("dark_theme", true);
//     setThemeFromCookie();
//     lightThemeButton.focus();
//   });

//   themeButtonsWrapper.appendChild(lightThemeButton);
//   themeButtonsWrapper.appendChild(darkThemeButton);
//   topNavigation.prepend(themeButtonsWrapper);
// };

// const removeThemeSwitcher = () => {
//   const themeSwitcher = document.getElementById("theme-switcher");
//   if (themeSwitcher) {
//     themeSwitcher.remove();
//   }
// };

// if (cookies.isPolicyAccepted("settings")) {
//   if (!cookies.exists("dark_theme")) {
//     setThemeCookieFromUserPref();
//   }
//   setThemeFromCookie();
//   addThemeSwitcher();
// } else {
//   setThemeFromUserPref();
// }

// cookies.on("changePolicy", (data) => {
//   if (Object.hasOwn(data, "settings")) {
//     if (data.settings === true) {
//       if (!cookies.exists("dark_theme")) {
//         setThemeCookieFromUserPref();
//       }
//       addThemeSwitcher();
//       setThemeFromCookie();
//     } else {
//       cookies.delete("dark_theme");
//       setThemeFromUserPref();
//       removeThemeSwitcher();
//     }
//   }
// });
