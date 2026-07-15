/* eslint-disable */
document.querySelectorAll(".tna-filters").forEach(($filters) => {
  $filters.querySelectorAll(".tna-filters__item").forEach(($item) => {
    const $toggleButton = $item.querySelector(".tna-filters__button");
    const $toggleButtonText =
      $toggleButton && $toggleButton.querySelector(".tna-filters__button-text");
    const $content = $item.querySelector(".tna-filters__content");
    if (!$toggleButton || !$toggleButtonText || !$content) {
      return;
    }
    let isExpanded = $toggleButton.getAttribute("aria-expanded") === "true";
    const update = () => {
      $toggleButton.setAttribute("aria-expanded", isExpanded.toString());
      if (isExpanded) {
        $content.removeAttribute("hidden");
        $toggleButtonText.textContent = "Hide";
      } else {
        $content.setAttribute("hidden", "");
        $toggleButtonText.textContent = "Show";
      }
    };
    const toggle = () => {
      isExpanded = !isExpanded;
      update();
    };
    $toggleButton.removeAttribute("hidden");
    $toggleButton.addEventListener("click", () => {
      toggle();
    });
    update();
  });
});
