const $articles = document.querySelectorAll(".etna-article");
$articles.forEach(($article) => {
  $article.classList.add("etna-article--interactive");

  const $collapsibleSections = $article.querySelector(
    ".etna-article__sections",
  );
  const $sections = $collapsibleSections.querySelectorAll(
    ".etna-article__section:has(h2:first-child)",
  );

  const targetSection = window.location.hash.replace(/^#/, "");
  const targetSectionExists = !!document.getElementById(targetSection);

  $sections.forEach(($section, index) => {
    const $heading = $section.querySelector("h2:first-child");
    const $buttonHeading = $section.previousElementSibling;

    if (
      !$heading ||
      !$buttonHeading ||
      !$buttonHeading.classList.contains("etna-article__section-button-header")
    ) {
      return;
    }

    const headingText = $heading.innerText;

    const $headingButton = $buttonHeading.querySelector(
      ".etna-article__section-button",
    );

    if (!$headingButton) {
      return;
    }

    $buttonHeading.removeAttribute("hidden");

    $headingButton.setAttribute("aria-controls", $heading.getAttribute("id"));

    const showSection = () => {
      $section.classList.remove("etna-article__section--hidden");
      $headingButton.setAttribute("aria-expanded", "true");
      $headingButton.setAttribute(
        "aria-label",
        `${headingText} - hide this section`,
      );
    };
    const hideSection = () => {
      $section.classList.add("etna-article__section--hidden");
      $headingButton.setAttribute("aria-expanded", "false");
      $headingButton.setAttribute(
        "aria-label",
        `${headingText} - show this section`,
      );
    };

    $headingButton.addEventListener("click", () =>
      $section.classList.contains("etna-article__section--hidden")
        ? showSection()
        : hideSection(),
    );

    $section.setAttribute("data-section-id", $heading.getAttribute("id"));

    if (
      (!targetSectionExists && index === 0) ||
      (targetSectionExists && $heading.getAttribute("id") === targetSection)
    ) {
      showSection();
      if (targetSectionExists) {
        setTimeout(() => {
          document.scrollingElement.scrollTo({
            top:
              $headingButton.getBoundingClientRect().y +
              document.scrollingElement.scrollTop,
            behavior: "smooth",
          });
        }, 100);
      }
    } else {
      hideSection();
    }
  });

  const $sidebar = $article.querySelector(".etna-article__sidebar");
  const $sidebarItems =
    $sidebar && $sidebar.querySelectorAll(".etna-article__sidebar-item");

  if ($sidebarItems) {
    let currentSectionId = "";
    const currentSectionFromTop = 0.05;
    const onMobile = window.matchMedia("(max-width: 48em)");

    const switchItemById = (targetItemID, $sidebarItems) => {
      const index = Array.from($sidebarItems).findIndex(
        ($sidebarItem) =>
          $sidebarItem.getAttribute("href") === `#${targetItemID}`,
      );
      if (index >= 0) {
        switchItem($sidebarItems[index], $sidebarItems);
      }
    };

    const switchItem = ($targetItem, $sidebarItems) => {
      const currentSectionHref = $targetItem.getAttribute("href");
      $sidebarItems.forEach(($sidebarItem) => {
        const isCurrentItem =
          $sidebarItem.getAttribute("href") === currentSectionHref;
        isCurrentItem
          ? $sidebarItem.classList.add("etna-article__sidebar-item--current")
          : $sidebarItem.classList.remove(
              "etna-article__sidebar-item--current",
            );
        if (isCurrentItem) {
          $sidebarItem.scrollIntoView({ block: "nearest" });
        }
      });
      if (history.replaceState) {
        history.replaceState(null, null, currentSectionHref);
      }
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
      const topSectionId =
        $topSection && $topSection.getAttribute("data-section-id");
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
          $sidebarItem.classList.remove("etna-article__sidebar-item--current");
        });
        if (history.replaceState) {
          history.replaceState(null, null, "#");
        }
      }
    };

    window.addEventListener("scroll", highlightCurrentSection);
    window.addEventListener("resize", highlightCurrentSection);
  }
});
