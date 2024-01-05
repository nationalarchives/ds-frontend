const $articles = document.querySelectorAll(".etna-article");
$articles.forEach(($article) => {
  $article.classList.add("etna-article--interactive");

  const $sidebar = $article.querySelector(".etna-article__sidebar");
  const $sidebarItems =
    $sidebar && $sidebar.querySelectorAll(".etna-article__sidebar-item");
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
      $headingButton.innerHTML = `<span class="etna-article__section-button-label">${headingText}</span><i class="fa-solid fa-chevron-up"></i>`;
    };
    const hideSection = () => {
      $section.classList.add("etna-article__section--hidden");
      $headingButton.setAttribute("aria-expanded", "false");
      $headingButton.setAttribute(
        "aria-label",
        `${headingText} - show this section`,
      );
      $headingButton.innerHTML = `<span class="etna-article__section-button-label">${headingText}</span><i class="fa-solid fa-chevron-down"></i>`;
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

  if ($sidebarItems) {
    let currentSectionId = "";
    const currentSectionFromTop = 0.15;
    const onMobile = window.matchMedia("(max-width: 48em)");
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
            $sidebarItems.forEach(($sidebarItem) =>
              $sidebarItem.getAttribute("href") === `#${currentSectionId}`
                ? $sidebarItem.classList.add(
                    "etna-article__sidebar-item--current",
                  )
                : $sidebarItem.classList.remove(
                    "etna-article__sidebar-item--current",
                  ),
            );
            if (history.replaceState) {
              history.replaceState(null, null, `#${currentSectionId}`);
            }
          }
        }
      } else {
        currentSectionId = "";
        $sidebarItems.forEach(($sidebarItem) =>
          $sidebarItem.classList.remove("etna-article__sidebar-item--current"),
        );
      }
    };

    window.addEventListener("scroll", highlightCurrentSection);
    window.addEventListener("resize", highlightCurrentSection);
  }
});
