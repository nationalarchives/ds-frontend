const $eventFiltersHeading = document.getElementById("event-filters-heading");
const $eventFilters = document.getElementById("event-filters");

if ($eventFiltersHeading && $eventFilters) {
  const $eventFiltersHeadingButton = document.createElement("button");
  $eventFiltersHeadingButton.setAttribute("type", "button");
  $eventFiltersHeadingButton.classList.add("tna-button");
  $eventFiltersHeadingButton.innerText = $eventFiltersHeading.innerText;
  $eventFiltersHeading.innerHTML = "";
  $eventFiltersHeading.appendChild($eventFiltersHeadingButton);
  $eventFiltersHeading.setAttribute("aria-controls", "event-filters");

  let wasOpenOnMobile = false;

  const showEventFilters = () => {
    $eventFiltersHeadingButton.innerHTML =
      '<i class="fa-solid fa-filter" aria-hidden="true"></i>Hide event filters';
    $eventFiltersHeading.setAttribute("aria-expanded", "true");
    $eventFilters.removeAttribute("hidden");
  };
  const hideEventFilters = () => {
    $eventFiltersHeadingButton.innerHTML =
      '<i class="fa-solid fa-filter" aria-hidden="true"></i>Show event filters';
    $eventFiltersHeading.setAttribute("aria-expanded", "false");
    $eventFilters.setAttribute("hidden", "");
  };

  const isMobile = window.matchMedia("(max-width: 48em)");
  isMobile.onchange = (e) => {
    if (e.matches) {
      if (wasOpenOnMobile) {
        showEventFilters();
      } else {
        hideEventFilters();
      }
    } else {
      showEventFilters();
    }
  };

  $eventFiltersHeadingButton.addEventListener("click", () => {
    const isExpanded =
      $eventFiltersHeading.getAttribute("aria-expanded") === "true";
    if (isExpanded) {
      hideEventFilters();
    } else {
      showEventFilters();
    }
    if (isMobile.matches) {
      wasOpenOnMobile = !isExpanded;
    }
  });

  if (isMobile.matches) {
    hideEventFilters();
  }
}
