export default class SectionsSidebarHighlighter {
  constructor($level2Headings, $sidebarItems) {
    if (!$level2Headings || !$sidebarItems) {
      return;
    }
    if ($level2Headings.length !== $sidebarItems.length) {
      throw "Sets are different sizes";
    }
    this.$level2Headings = $level2Headings;
    this.$sidebarItems = $sidebarItems;
    this.currentSectionFromTop = 0.05;
    this.currentSectionId = "";
    this.onMobile = window.matchMedia("(max-width: 48em)");
    window.addEventListener("scroll", () => this.highlightCurrentSection());
    window.addEventListener("resize", () => this.highlightCurrentSection());
  }

  switchItemById(targetItemID) {
    const index = Array.from(this.$sidebarItems).findIndex(
      ($sidebarItem) =>
        $sidebarItem.querySelector("a[href]").getAttribute("href") ===
        `#${targetItemID}`,
    );
    if (index >= 0) {
      this.switchItem(this.$sidebarItems[index]);
    }
  }

  switchItem($targetItem) {
    const currentSectionHref = $targetItem
      .querySelector("a[href]")
      .getAttribute("href");
    this.$sidebarItems.forEach(($sidebarItem) => {
      const isCurrentItem =
        $sidebarItem.querySelector("a[href]").getAttribute("href") ===
        currentSectionHref;
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
  }

  highlightCurrentSection() {
    if (this.onMobile.matches) {
      this.$sidebarItems.forEach(($sidebarItem) => {
        $sidebarItem.classList.remove("tna-sidebar__item--current");
      });
      return;
    }
    const $topHeading = Array.from(this.$level2Headings)
      .reverse()
      .find(
        ($section) =>
          $section.getBoundingClientRect().top <
          window.innerHeight * this.currentSectionFromTop,
      );
    const topHeadingId = $topHeading && $topHeading.id;
    if (topHeadingId) {
      if (topHeadingId !== this.currentSectionId) {
        this.currentSectionId = topHeadingId;
        if ($topHeading) {
          this.switchItemById(this.currentSectionId);
          // if (history.replaceState) {
          //   history.replaceState(null, null, `#${this.currentSectionId}`);
          // }
        }
      }
    } else {
      this.currentSectionId = "";
      this.$sidebarItems.forEach(($sidebarItem) => {
        $sidebarItem.classList.remove("tna-sidebar__item--current");
      });
      // if (history.replaceState) {
      //   history.replaceState(null, null, "#");
      // }
    }
  }
}
