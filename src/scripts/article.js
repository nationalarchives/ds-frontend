const $article = document.querySelector(".etna-article");
$article.classList.add("etna-article--interactive");

const $collapsibleSections = $article.querySelector(".etna-article__sections");
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

$article
  .querySelectorAll(".tna-picture__image-wrapper")
  .forEach(($imageWrapper) => {
    $imageWrapper.addEventListener("dblclick", () => {
      if (!document.fullscreenElement) {
        $imageWrapper.requestFullscreen();
      } else if (document.exitFullscreen) {
        document.exitFullscreen();
      }
    });
  });
