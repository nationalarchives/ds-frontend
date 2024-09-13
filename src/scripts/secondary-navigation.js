const $secondaryNavigation = document.getElementById("secondary-navigation");
const $pageBody = document.getElementById("page-body");
if ($secondaryNavigation && $pageBody) {
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
    return {
      listItem: $pageSectionItem,
      button: $pageSectionItemLink,
      id,
      section: $pageBody.querySelector(`[data-sectionfor="${id}"]`),
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
        section.section.removeAttribute("hidden");
        section.section.setAttribute("tabindex", "0");
        section.button.setAttribute("tabindex", "0");
        if (switchFocus) {
          section.button.focus();
        }
        section.listItem.classList.add(
          "etna-secondary-navigation__item--current",
        );
      } else {
        section.section.setAttribute("hidden", "until-found");
        section.section.setAttribute("tabindex", "-1");
        section.button.setAttribute("tabindex", "-1");
        section.listItem.classList.remove(
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
      $sectionsPaginationPreviousText.innerText =
        sections[selectedIndex - 1].button.innerText;
    } else {
      $sectionsPaginationPrevious.setAttribute("hidden", true);
    }
    if (selectedIndex + 1 < sections.length) {
      $sectionsPaginationNext.removeAttribute("hidden");
      $sectionsPaginationNext.setAttribute(
        "aria-controls",
        sections[selectedIndex + 1].id,
      );
      $sectionsPaginationNextText.innerText =
        sections[selectedIndex + 1].button.innerText;
    } else {
      $sectionsPaginationNext.setAttribute("hidden", true);
    }
  };
  sections.forEach((section, index) => {
    section.section.setAttribute("role", "tabpanel");
    section.section.setAttribute("aria-labelledby", section.button.id);
    section.button.addEventListener("click", () => {
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
  $sectionsPaginationPrevious?.addEventListener("click", () => {
    previousSection(false);
    updatePaginationLabels();
    sections[selectedIndex].section.focus();
  });
  $sectionsPaginationNext?.addEventListener("click", () => {
    nextSection(false);
    updatePaginationLabels();
    sections[selectedIndex].section.focus();
  });
  updatePaginationLabels();
}
