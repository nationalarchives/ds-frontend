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
    $heading.classList.add("etna-article__section-heading");
    const headingText = $heading.innerText;

    const $headingButton = document.createElement("button");
    $headingButton.classList.add(
      "etna-article__section-button",
      "tna-heading-l",
    );

    const showSection = () => {
      $section.classList.remove("etna-article__section--hidden");
      $headingButton.setAttribute("aria-expanded", "true");
      $headingButton.setAttribute(
        "aria-label",
        `${headingText} - hide this section`,
      );
      $headingButton.innerHTML = `<h2 class="etna-article__section-button-label">${headingText}</h2><i class="fa-solid fa-chevron-up"></i>`;
    };
    const hideSection = () => {
      $section.classList.add("etna-article__section--hidden");
      $headingButton.setAttribute("aria-expanded", "false");
      $headingButton.setAttribute(
        "aria-label",
        `${headingText} - show this section`,
      );
      $headingButton.innerHTML = `<h2 class="etna-article__section-button-label">${headingText}</h2><i class="fa-solid fa-chevron-down"></i>`;
    };

    $headingButton.addEventListener("click", () =>
      $section.classList.contains("etna-article__section--hidden")
        ? showSection()
        : hideSection(),
    );

    $collapsibleSections.insertBefore($headingButton, $section);
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
    const currentSectionFromTop = 0.15;
    const onMobile = window.matchMedia("(max-width: 48em)");

    // const setSelectedToPreviousItem = ($targetItem, $sidebarItems) => {
    //   const currentIndex = Array.from($sidebarItems).findIndex(($sidebarItem) =>
    //       $sidebarItem.getAttribute("href") === $targetItem.getAttribute("href")
    //   )
    //   if(currentIndex > 0) {
    //     switchItemByIndex(currentIndex - 1,$sidebarItems, true)
    //   }
    // }

    // const setSelectedToNextItem = ($targetItem,$sidebarItems) => {
    //   const currentIndex = Array.from($sidebarItems).findIndex(($sidebarItem) =>
    //       $sidebarItem.getAttribute("href") === $targetItem.getAttribute("href")
    //   )
    //   if(currentIndex < $sidebarItems.length - 1) {
    //     switchItemByIndex(currentIndex + 1,$sidebarItems, true)
    //   }
    // }

    // const switchItemByIndex = (
    //   targetItemIndex,
    //   $sidebarItems,
    //   simulateClick = false,
    // ) => {
    //   switchItem($sidebarItems[targetItemIndex], $sidebarItems, true);
    // };

    const switchItemById = (
      targetItemID,
      $sidebarItems,
      // simulateClick = false,
    ) => {
      const index = Array.from($sidebarItems).findIndex(
        ($sidebarItem) =>
          $sidebarItem.getAttribute("href") === `#${targetItemID}`,
      );
      if (index >= 0) {
        switchItem($sidebarItems[index], $sidebarItems /*, simulateClick*/);
      }
    };

    const switchItem = (
      $targetItem,
      $sidebarItems /*, simulateClick = false*/,
    ) => {
      const currentSectionHref = $targetItem.getAttribute("href");
      $sidebarItems.forEach(($sidebarItem) => {
        const isCurrentItem =
          $sidebarItem.getAttribute("href") === currentSectionHref;
        isCurrentItem
          ? $sidebarItem.classList.add("etna-article__sidebar-item--current")
          : $sidebarItem.classList.remove(
              "etna-article__sidebar-item--current",
            );
        // $sidebarItem.setAttribute("tabindex", isCurrentItem ? "0" : "-1");
      });
      if (history.replaceState) {
        history.replaceState(null, null, currentSectionHref);
      }
      // if (simulateClick) {
      //   // $targetItem.click()
      // } else {
      //   $targetItem.focus();
      // }
    };

    // const handleSidebarItemKeyDown = (e, $sidebarItems) => {
    //   const targetItem = e.currentTarget;
    //   let overwriteKeyAction = false;

    //   switch (e.key) {
    //     case "ArrowUp":
    //       setSelectedToPreviousItem(targetItem, $sidebarItems);
    //       overwriteKeyAction = true;
    //       break;

    //     case "ArrowDown":
    //       setSelectedToNextItem(targetItem, $sidebarItems);
    //       overwriteKeyAction = true;
    //       break;

    //     case "Home":
    //       switchItem(0);
    //       overwriteKeyAction = true;
    //       break;

    //     case "End":
    //       switchItem($sidebarItems.length - 1);
    //       overwriteKeyAction = true;
    //       break;

    //     default:
    //       break;
    //   }

    //   if (overwriteKeyAction) {
    //     e.stopPropagation();
    //     e.preventDefault();
    //   }
    // };

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
            // $sidebarItems.forEach(($sidebarItem) => {
            //   const isCurrentItem =
            //     $sidebarItem.getAttribute("href") === `#${currentSectionId}`;
            //   isCurrentItem
            //     ? $sidebarItem.classList.add(
            //         "etna-article__sidebar-item--current",
            //       )
            //     : $sidebarItem.classList.remove(
            //         "etna-article__sidebar-item--current",
            //       );
            //   // $sidebarItem.setAttribute("tabindex", isCurrentItem ? "0" : "-1");
            // });
            // if (history.replaceState) {
            //   history.replaceState(null, null, `#${currentSectionId}`);
            // }
          }
        }
      } else {
        currentSectionId = "";
        // $sidebarItems.forEach(($sidebarItem, index) => {
        //   $sidebarItem.classList.remove("etna-article__sidebar-item--current");
        //   $sidebarItem.setAttribute("tabindex", index === 0 ? "0" : "-1");
        // });
        $sidebarItems.forEach(($sidebarItem) => {
          $sidebarItem.classList.remove("etna-article__sidebar-item--current");
        });
        if (history.replaceState) {
          history.replaceState(null, null, "#");
        }
      }
    };

    // $sidebarItems.forEach(($sidebarItem) => {
    //   $sidebarItem.addEventListener(
    //     "keydown",
    //     (e) => handleSidebarItemKeyDown(e, $sidebarItems),
    //     true,
    //   );
    // });

    window.addEventListener("scroll", highlightCurrentSection);
    window.addEventListener("resize", highlightCurrentSection);
  }
});
