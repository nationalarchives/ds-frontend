const $secondaryNavigation = document.getElementById("secondary-navigation");
const $pageBody = document.getElementById("page-body");
if ($secondaryNavigation && $pageBody) {
  if ($secondaryNavigation.hasAttribute("hidden")) {
    $secondaryNavigation.removeAttribute("hidden");
    const $pageContentsList = document.getElementById("page-contents-list");
    if ($pageContentsList) {
      $pageContentsList.setAttribute("hidden", true);
    }
    const sections = Array.from(
      $secondaryNavigation.querySelectorAll("li:has(button[aria-controls])"),
    ).map(($pageSectionItem) => {
      const $pageSectionItemLink = $pageSectionItem.querySelector("button");
      const id = $pageSectionItemLink.getAttribute("aria-controls");
      const $section = $pageBody.querySelector(`[data-sectionfor="${id}"]`);
      return {
        $listItem: $pageSectionItem,
        $button: $pageSectionItemLink,
        id,
        $section: $section,
      };
    });
    let selectedIndex = sections.findIndex(
      (section) => `#${section.id}` === window.location.hash,
    );
    if (selectedIndex < 0) {
      selectedIndex = 0;
    }
    const showSectionByIndex = (indexToShow, switchFocus = false) => {
      selectedIndex = indexToShow;
      sections.forEach((section, index) => {
        if (index === indexToShow) {
          section.$section.removeAttribute("hidden");
          section.$section.setAttribute("tabindex", "0");
          section.$button.setAttribute("tabindex", "0");
          section.$button.setAttribute("aria-selected", "true");
          if (switchFocus) {
            section.$button.focus();
          }
          section.$listItem.classList.add(
            "etna-secondary-navigation__item--current",
          );
        } else {
          section.$section.setAttribute("hidden", "until-found");
          section.$section.setAttribute("tabindex", "-1");
          section.$button.setAttribute("tabindex", "-1");
          section.$button.setAttribute("aria-selected", "false");
          section.$listItem.classList.remove(
            "etna-secondary-navigation__item--current",
          );
        }
      });
      updatePaginationLabels();
    };
    const previousSection = (switchFocus = true) => {
      if (selectedIndex >= 1) {
        showSectionByIndex(selectedIndex - 1, switchFocus);
      } else {
        showSectionByIndex(sections.length - 1, switchFocus);
      }
    };
    const nextSection = (switchFocus = true) => {
      if (selectedIndex < sections.length - 1) {
        showSectionByIndex(selectedIndex + 1, switchFocus);
      } else {
        showSectionByIndex(0, switchFocus);
      }
    };
    const $sectionsPagination = document.getElementById(
      "page-section-navigation",
    );
    const $sectionsPaginationPrevious = document.getElementById(
      "page-section-navigation__previous",
    );
    const $sectionsPaginationPreviousText = document.getElementById(
      "page-section-navigation__previous-text",
    );
    // const $sectionsPaginationCurrentText = document.getElementById(
    //   "page-section-navigation__current-item-text",
    // );
    const $sectionsPaginationNext = document.getElementById(
      "page-section-navigation__next",
    );
    const $sectionsPaginationNextText = document.getElementById(
      "page-section-navigation__next-text",
    );
    const updatePaginationLabels = () => {
      if (selectedIndex > 0) {
        $sectionsPaginationPrevious.removeAttribute("hidden");
        $sectionsPaginationPrevious.setAttribute(
          "aria-controls",
          sections[selectedIndex - 1].id,
        );
        // $sectionsPaginationPreviousText.innerHTML =
        //   `Previous:<br>${sections[selectedIndex - 1].$button.innerText}`;
        $sectionsPaginationPreviousText.innerText = `Previous: ${sections[selectedIndex - 1].$button.innerText}`;
      } else {
        $sectionsPaginationPrevious.setAttribute("hidden", true);
      }
      if (selectedIndex + 1 < sections.length) {
        $sectionsPaginationNext.removeAttribute("hidden");
        $sectionsPaginationNext.setAttribute(
          "aria-controls",
          sections[selectedIndex + 1].id,
        );
        // $sectionsPaginationNextText.innerHTML =
        //   `Next:<br>${sections[selectedIndex + 1].$button.innerText}`;
        $sectionsPaginationNextText.innerText = `Next: ${sections[selectedIndex + 1].$button.innerText}`;
      } else {
        $sectionsPaginationNext.setAttribute("hidden", true);
      }
      // $sectionsPaginationCurrentText.innerText = sections[selectedIndex].$button.innerText;
      // $sectionsPaginationCurrentText.innerText = `Section ${selectedIndex + 1} of ${sections.length}`;
    };
    sections.forEach((section, index) => {
      section.$section.setAttribute("role", "tabpanel");
      section.$section.setAttribute("aria-labelledby", section.$button.id);
      section.$button.addEventListener("click", () => {
        showSectionByIndex(index, true);
        window.history.replaceState(null, null, `#${section.id}`);
      });
    });
    showSectionByIndex(selectedIndex);
    $secondaryNavigation.addEventListener("keydown", (e) => {
      let preventDefaultKeyAction = false;
      switch (e.key) {
        case "ArrowLeft":
        case "ArrowUp":
          previousSection();
          preventDefaultKeyAction = true;
          break;
        case "ArrowRight":
        case "ArrowDown":
          nextSection();
          preventDefaultKeyAction = true;
          break;
        case "Home":
          showSectionByIndex(0, true);
          preventDefaultKeyAction = true;
          break;
        case "End":
          showSectionByIndex(sections.length - 1, true);
          preventDefaultKeyAction = true;
          break;
        default:
          break;
      }
      if (preventDefaultKeyAction) {
        e.stopPropagation();
        e.preventDefault();
      }
    });
    $sectionsPagination?.removeAttribute("hidden");
    const postSectionsPaginationClick = () => {
      updatePaginationLabels();
      const $section = sections[selectedIndex].$section;
      const $heading = $section.querySelector("h2:first-child[id]");
      window.history.replaceState(null, null, `#${$heading.id}`);
      $heading.scrollIntoView({ block: "nearest" });
      $section.focus();
    };
    $sectionsPaginationPrevious?.addEventListener("click", () => {
      previousSection(false);
      postSectionsPaginationClick();
    });
    $sectionsPaginationNext?.addEventListener("click", () => {
      nextSection(false);
      postSectionsPaginationClick();
    });
    updatePaginationLabels();
  }

  const checkSecondaryNavigationForScroll = ($secondaryNavigationToCheck) => {
    console.log("checkSecondaryNavigationForScroll");
    console.log($secondaryNavigationToCheck);
    console.log($secondaryNavigationToCheck.scrollWidth);
    console.log($secondaryNavigationToCheck.clientWidth);
    const scrollable =
      $secondaryNavigationToCheck.scrollWidth >
      $secondaryNavigationToCheck.clientWidth;
    console.log(scrollable);
    if (scrollable) {
      $secondaryNavigationToCheck.classList.add(
        "etna-secondary-navigation--overflow",
      );
    } else {
      $secondaryNavigationToCheck.classList.remove(
        "etna-secondary-navigation--overflow",
      );
    }
  };

  checkSecondaryNavigationForScroll($secondaryNavigation);
  window.addEventListener("resize", () => {
    checkSecondaryNavigationForScroll($secondaryNavigation);
  });
}
