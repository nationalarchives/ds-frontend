import { initAll } from "@nationalarchives/frontend/nationalarchives/all.mjs";
// import {GA4} from "@nationalarchives/frontend/nationalarchives/analytics.mjs";

initAll();

/*
 * ==========================================
 * TEMP: ANALYTICS
 * ==========================================
 */
// const TNAAnalytics = window.TNAFrontendAnalytics
// const analytics = new TNAAnalytics.GA4("GTM-KX8ZWVZG");

// analytics.addListener(".etna-article__sidebar", "sidebar", [
//   {
//     eventName: "scection_jump",
//     targetElement: ".etna-article__sidebar-item",
//     on: "click",
//     data: {
//       value: TNAAnalytics.helpers.valueGetters.text,
//     },
//   },
// ]);

// analytics.addListener(".etna-article", "article", [
//   {
//     eventName: "toggle_section",
//     targetElement: ".etna-article__section-button",
//     on: "click",
//     data: {
//       // eslint-disable-next-line no-unused-vars
//       state: ($el, $scope, event) => {
//         const expanded = $el.getAttribute("aria-expanded");
//         if (expanded === null) {
//           return null;
//         }
//         return expanded.toString() === "true" ? "opened" : "closed";
//       },
//       value: TNAAnalytics.helpers.valueGetters.text,
//     },
//   },
// ]);

// analytics.addListener(document.documentElement, "doc", [
//   {
//     eventName: "double_click",
//     on: "dblclick",
//     data: {
//       state: ($el, $scope, event) => getXPathTo(event.target),
//       value: ($el, $scope, event) => event.target.innerHTML,
//     },
//   },
// ]);

// analytics.addListener(document.getElementById("tna-form__search"), "search", [
//   {
//     eventName: "search_term_blur",
//     on: "blur",
//     data: {
//       value: TNAAnalytics.helpers.valueGetters.value,
//     },
//   },
// ]);

/*
 * ==========================================
 * TEMP: NEW HEADER
 * ==========================================
 */
document.querySelectorAll(".tna-global-header").forEach((header) => {
  const $menuButtonWrapper = header.querySelector(
    ".tna-global-header__menu-button-wrapper",
  );
  const $menuButton = document.createElement("button");
  $menuButton.classList.add("tna-global-header__menu-button");
  $menuButton.innerText = "Menu";
  $menuButton.addEventListener("click", () => {
    console.log("click");
  });
  $menuButtonWrapper.appendChild($menuButton);
  const $menuNavigationDisclosure = header.querySelector(
    ".tna-global-header__disclosure",
  );
  const $menuNavigationItemTitleLinks = header.querySelectorAll(
    ".tna-global-header__navigation-item-link",
  );
  $menuNavigationItemTitleLinks.forEach(($itemTitleLink) => {
    const $item = $itemTitleLink.closest(".tna-global-header__navigation-item");
    if ($item) {
      const $itemContents = $item.querySelector(
        ".tna-global-header__navigation-item-contents",
      );

      const $itemChildren = $item.querySelector(
        ".tna-global-header__navigation-item-children",
      );
      if ($itemChildren) {
        $itemChildren.setAttribute("hidden", true);
      }

      if ($itemContents) {
        $itemContents.setAttribute("hidden", true);
        $itemTitleLink.addEventListener("click", (e) => {
          e.preventDefault();
          if ($itemChildren) {
            if ($itemChildren.hasAttribute("hidden")) {
              $itemChildren.removeAttribute("hidden");
            } else {
              $itemChildren.setAttribute("hidden", true);
            }
          }

          $menuNavigationDisclosure.innerHTML = $item.innerHTML;
          const $itemContentsCopy = $menuNavigationDisclosure.querySelector(
            ".tna-global-header__navigation-item-contents[hidden]",
          );
          if ($itemContentsCopy) {
            $itemContentsCopy.removeAttribute("hidden");
          }
          const $itemChildrenCopy = $menuNavigationDisclosure.querySelector(
            ".tna-global-header__navigation-item-children[hidden]",
          );
          if ($itemChildrenCopy) {
            $itemChildrenCopy.removeAttribute("hidden");
          }
          const $itemHeaderCopy = $menuNavigationDisclosure.querySelector(
            ".tna-global-header__navigation-item-heading",
          );
          if ($itemHeaderCopy) {
            $itemHeaderCopy.classList.remove(
              "tna-global-header__navigation-item-heading",
            );
            $itemHeaderCopy.classList.add("tna-heading-l");
          }
          const $closeDisclosure = document.createElement("button");
          $closeDisclosure.innerText = "Close";
          $closeDisclosure.classList.add(
            "tna-global-header__disclosure-close-button",
          );
          $closeDisclosure.addEventListener("click", () => {
            $menuNavigationDisclosure.innerHTML = "";
            // $menuNavigationDisclosure.classList.remove("tna-section");
          });
          // $menuNavigationDisclosure.classList.add("tna-section");
          $menuNavigationDisclosure.append($closeDisclosure);
          $menuNavigationDisclosure.focus();
        });
      }
    }
  });
});
