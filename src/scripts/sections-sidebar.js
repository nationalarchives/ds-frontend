const $allSections = document
  .getElementById("main-content")
  .querySelector(".etna-article__sections");
const $sections = $allSections.querySelectorAll(
  ".etna-article__section:has(h2:first-child)",
);

const $sidebar = document
  .getElementById("main-content")
  .querySelector(".tna-sidebar");
const $sidebarItems =
  $sidebar && $sidebar.querySelectorAll(".tna-sidebar__item");

console.log($sidebarItems);

if ($sidebarItems) {
  let currentSectionId = "";
  const currentSectionFromTop = 0.05;
  const onMobile = window.matchMedia("(max-width: 48em)");

  const switchItemById = (targetItemID, $sidebarItems) => {
    const index = Array.from($sidebarItems).findIndex(
      ($sidebarItem) =>
        $sidebarItem
          .querySelector(".tna-sidebar__link")
          .getAttribute("href") === `#${targetItemID}`,
    );
    if (index >= 0) {
      switchItem($sidebarItems[index], $sidebarItems);
    }
  };

  const switchItem = ($targetItem, $sidebarItems) => {
    const currentSectionHref = $targetItem
      .querySelector(".tna-sidebar__link")
      .getAttribute("href");
    $sidebarItems.forEach(($sidebarItem) => {
      const isCurrentItem =
        $sidebarItem
          .querySelector(".tna-sidebar__link")
          .getAttribute("href") === currentSectionHref;
      isCurrentItem
        ? $sidebarItem.classList.add("tna-sidebar__item--current")
        : $sidebarItem.classList.remove("tna-sidebar__item--current");
      if (isCurrentItem) {
        $sidebarItem.scrollIntoView({ block: "nearest" });
      }
    });
    // if (history.replaceState) {
    //   history.replaceState(null, null, currentSectionHref);
    // }
  };

  const highlightCurrentSection = () => {
    if (onMobile.matches) {
      return;
    }
    const $topSection = Array.from($sections)
      .reverse()
      .find(
        ($section) =>
          $section.getBoundingClientRect().top <
          window.innerHeight * currentSectionFromTop,
      );
    console.log($topSection);
    const topSectionId =
      $topSection && $topSection.querySelector("h2:first-child").id;
    console.log(topSectionId);
    if (topSectionId) {
      if (topSectionId !== currentSectionId) {
        currentSectionId = topSectionId;
        if ($topSection) {
          switchItemById(currentSectionId, $sidebarItems);
          // if (history.replaceState) {
          //   history.replaceState(null, null, `#${currentSectionId}`);
          // }
        }
      }
    } else {
      currentSectionId = "";
      $sidebarItems.forEach(($sidebarItem) => {
        $sidebarItem.classList.remove("tna-sidebar__item--current");
      });
      // if (history.replaceState) {
      //   history.replaceState(null, null, "#");
      // }
    }
  };

  window.addEventListener("scroll", highlightCurrentSection);
  window.addEventListener("resize", highlightCurrentSection);
}
