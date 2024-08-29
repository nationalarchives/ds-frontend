import SectionsSidebarHighlighter from "./lib/sections-sidebar";

const $level2Headings = document
  .getElementById("page-body")
  ?.querySelectorAll("h2[id]");
const $sidebarItems = document
  .getElementById("page-sidebar")
  ?.querySelectorAll(".tna-sidebar__item");
if ($level2Headings && $sidebarItems) {
  new SectionsSidebarHighlighter($level2Headings, $sidebarItems);
}

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
  };
  const previousSection = () => {
    if (selectedIndex >= 1) {
      showSectionByIndex(selectedIndex - 1, true);
    } else {
      showSectionByIndex(sections.length - 1, true);
    }
  };
  const nextSection = () => {
    if (selectedIndex < sections.length - 1) {
      showSectionByIndex(selectedIndex + 1, true);
    } else {
      showSectionByIndex(0, true);
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
}
