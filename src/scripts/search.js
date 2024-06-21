const $searchFiltersContent = document.getElementById("search-filters");
if ($searchFiltersContent) {
  const updateExpandContractButtonText = (
    $button,
    expanded,
    filtersSelected,
  ) => {
    if (expanded) {
      $button.innerText = "Hide filters";
    } else if (filtersSelected) {
      $button.innerText = `Edit filters (${filtersSelected})`;
    } else {
      $button.innerText = "Add filters";
    }
  };

  let expandedFilters = false;
  const filtersSelected = parseInt(
    $searchFiltersContent.getAttribute("data-selectedfilters") ?? "0",
  );
  const $searchFiltersWrapper = document.createElement("div");
  $searchFiltersContent.parentNode.insertBefore(
    $searchFiltersWrapper,
    $searchFiltersContent,
  );
  $searchFiltersWrapper.appendChild($searchFiltersContent);
  $searchFiltersWrapper.setAttribute(
    "class",
    $searchFiltersContent.getAttribute("class"),
  );
  $searchFiltersContent.setAttribute("class", "etna-search-sidebar__content");

  const $filtersExpandContractButton = document.createElement("button");
  updateExpandContractButtonText(
    $filtersExpandContractButton,
    expandedFilters,
    filtersSelected,
  );
  $filtersExpandContractButton.classList.add(
    "tna-button",
    "tna-!--margin-bottom-s",
    "etna-search-sidebar__expand-button",
  );
  $filtersExpandContractButton.addEventListener("click", () => {
    expandedFilters = !expandedFilters;
    if (expandedFilters) {
      $searchFiltersContent.classList.add(
        "etna-search-sidebar__content--expanded",
      );
    } else {
      $searchFiltersContent.classList.remove(
        "etna-search-sidebar__content--expanded",
      );
    }
    updateExpandContractButtonText(
      $filtersExpandContractButton,
      expandedFilters,
      filtersSelected,
    );
  });
  $searchFiltersContent.parentNode.insertBefore(
    $filtersExpandContractButton,
    $searchFiltersContent,
  );
}

const $sortView = document.querySelector(".etna-search-sort-view");
const $orderSelect = document.getElementById("tna-form__order");
const $searchForm = document.getElementById("search-form");
if ($sortView && $orderSelect && $searchForm) {
  const $sortViewButtonGroup = $sortView.querySelector(".tna-button-group");
  if ($sortViewButtonGroup) {
    $sortViewButtonGroup.remove();
    $orderSelect.addEventListener("change", () => {
      $searchForm.submit();
    });
  }
}
