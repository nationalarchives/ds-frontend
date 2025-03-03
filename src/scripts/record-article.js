class Gallery {
  constructor($module) {
    this.$module = $module;
    this.$items =
      $module && $module.querySelector(".etna-record-gallery__items");
    this.opened = false;

    if (!this.$items) {
      return;
    }

    this.itemsCount = this.$module.querySelectorAll(
      ".etna-record-gallery__item",
    ).length;

    if (this.itemsCount > 1) {
      const id = `tna-record-article-gallery`;

      this.$module.classList.add("etna-record-gallery--collapsed");
      this.$items.setAttribute("tabindex", "-1");

      this.$galleryToggle = document.createElement("button");
      this.$galleryToggle.classList.add(
        "etna-record-gallery__toggle",
        "tna-button",
        "tna-button--accent",
      );
      this.$galleryToggle.setAttribute("type", "button");
      this.$galleryToggle.setAttribute("aria-controls", id);
      this.$galleryToggle.setAttribute("aria-expanded", false);
      this.$galleryToggle.innerText = `View ${this.itemsCount} images`;

      //   const onFirstTouch = () => {
      //     this.$module.removeEventListener("touchstart", onFirstTouch);
      //     this.$module.classList.add("etna-record-gallery--touchable");
      //   };

      //   this.$module.addEventListener("touchstart", onFirstTouch);

      this.$galleryToggle.addEventListener("click", () => {
        // this.$module.removeEventListener("touchstart", onFirstTouch);
        this.handleToggleGallery();
      });

      this.$galleryToggleWrapper = document.createElement("div");
      this.$galleryToggleWrapper.classList.add(
        "tna-column",
        "tna-column--full",
        "etna-record-gallery__toggle-wrapper",
      );

      this.$galleryToggleWrapper.appendChild(this.$galleryToggle);
      this.$items.parentElement.appendChild(this.$galleryToggleWrapper);

      this.$items.setAttribute("id", id);
    }
  }

  handleToggleGallery() {
    this.opened = !this.opened;
    if (this.opened) {
      this.$module.classList.remove("etna-record-gallery--collapsed");
      this.$galleryToggle.setAttribute("aria-expanded", true);
      this.$galleryToggle.innerText = "Close images";
      this.$items.setAttribute("tabindex", "0");
      this.$items.focus();
      this.$items.setAttribute("tabindex", "-1");
    } else {
      this.$module.classList.add("etna-record-gallery--collapsed");
      this.$galleryToggle.setAttribute("aria-expanded", false);
      this.$galleryToggle.innerText = `View ${this.itemsCount} images`;
    }
  }
}

const $gallery = document.querySelector(".etna-record-gallery");
if ($gallery) {
  new Gallery($gallery);
}
