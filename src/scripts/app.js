import {
  initAll,
  Cookies,
} from "@nationalarchives/frontend/nationalarchives/all.mjs";

window.TNAFrontend = { Cookies };

initAll();

/*
 * ==========================================
 * TEMP: NEW HEADER
 * ==========================================
 */
document.querySelectorAll(".tna-new-header").forEach((header) => {
  const $menuButtonWrapper = header.querySelector(
    ".tna-new-header__menu-button-wrapper",
  );
  const $menuButton = document.createElement("button");
  $menuButton.classList.add("tna-new-header__menu-button");
  $menuButton.innerText = "Menu";
  $menuButton.addEventListener("click", () => {
    console.log("click");
  });
  $menuButtonWrapper.appendChild($menuButton);
  const $menuNavigationDisclosure = header.querySelector(
    ".tna-new-header__disclosure",
  );
  const $menuNavigationItemTitleLinks = header.querySelectorAll(
    ".tna-new-header__navigation-item-link",
  );
  $menuNavigationItemTitleLinks.forEach(($itemTitleLink) => {
    const $item = $itemTitleLink.closest(".tna-new-header__navigation-item");
    if ($item) {
      const $itemContents = $item.querySelector(
        ".tna-new-header__navigation-item-contents",
      );

      const $itemChildren = $item.querySelector(
        ".tna-new-header__navigation-item-children",
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
            ".tna-new-header__navigation-item-contents[hidden]",
          );
          if ($itemContentsCopy) {
            $itemContentsCopy.removeAttribute("hidden");
          }
          const $itemChildrenCopy = $menuNavigationDisclosure.querySelector(
            ".tna-new-header__navigation-item-children[hidden]",
          );
          if ($itemChildrenCopy) {
            $itemChildrenCopy.removeAttribute("hidden");
          }
          const $itemHeaderCopy = $menuNavigationDisclosure.querySelector(
            ".tna-new-header__navigation-item-heading",
          );
          if ($itemHeaderCopy) {
            $itemHeaderCopy.classList.remove(
              "tna-new-header__navigation-item-heading",
            );
            $itemHeaderCopy.classList.add("tna-heading-l");
          }
          const $closeDisclosure = document.createElement("button");
          $closeDisclosure.innerText = "Close";
          $closeDisclosure.classList.add(
            "tna-new-header__disclosure-close-button",
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
