import {
  GA4,
  helpers,
} from "@nationalarchives/frontend/nationalarchives/analytics.mjs";

const ga4Id = document.documentElement.getAttribute("data-ga4id");
if (ga4Id) {
  const analytics = new GA4({ id: ga4Id });

  // analytics.addListeners(".etna-article", "article", [
  //   {
  //     eventName: "section.toggle",
  //     targetElement: ".etna-article__section-button",
  //     on: "click",
  //     data: {
  //       state: helpers.valueGetters.expanded,
  //       value: helpers.valueGetters.text,
  //     },
  //   },
  // ]);

  analytics.addListeners("body", "page", [
    {
      eventName: "double_click",
      on: "dblclick",
      data: {
        state: ($el, $scope, event) => helpers.getXPathTo(event.target),
      },
    },
    {
      eventName: "cta.click",
      targetElement: ".tna-button[data-tna-cta]",
      on: "click",
      rootData: {
        data_link: helpers.valueGetters.text,
        data_component_name: "button",
        data_link_type: "button",
        event: "tna.select_cta",
      },
    },
    {
      eventName: "chip.click",
      targetElement: ".tna-hgroup__supertitle",
      on: "click",
      data: {
        value: helpers.valueGetters.text,
      },
    },
    {
      eventName: "chip.click",
      targetElement: ".tna-chip",
      on: "click",
      data: {
        value: helpers.valueGetters.text,
      },
    },
    {
      eventName: "tel.click",
      targetElement: "a[href^='tel:']",
      on: "click",
      data: {
        value: helpers.valueGetters.text,
      },
    },
    {
      eventName: "mailto.click",
      targetElement: "a[href^='mailto:']",
      on: "click",
      data: {
        value: helpers.valueGetters.text,
      },
    },
  ]);

  const componentFromElement = ($el) => {
    if ($el.classList.contains("tna-card__heading-link")) {
      return "card";
    } else if ($el.classList.contains("tna-button")) {
      return "button";
    } else if (
      $el.parentNode.classList.contains("tna-heading-xl") ||
      $el.parentNode.classList.contains("tna-heading-l") ||
      $el.parentNode.classList.contains("tna-heading-m") ||
      $el.parentNode.classList.contains("tna-heading-s")
    ) {
      return "title_link";
    }
    return "link";
  };

  const linkTypeFromElement = ($el) => {
    if ($el.classList.contains("tna-card__heading-link")) {
      const $card = $el.closest(".tna-card");
      if ($card.querySelector(".tna-card__image-container")) {
        return "card";
      }
      return "card_no_image";
    } else if ($el.classList.contains("tna-card__action")) {
      return "card_action";
    } else if ($el.classList.contains("tna-button")) {
      return "button";
    } else if (
      $el.parentNode.classList.contains("tna-heading-xl") ||
      $el.parentNode.classList.contains("tna-heading-l") ||
      $el.parentNode.classList.contains("tna-heading-m") ||
      $el.parentNode.classList.contains("tna-heading-s")
    ) {
      return "title_link";
    }
    return "link";
  };

  analytics.addListeners("[data-tna-analytics-section]", "html-attr-scope", [
    {
      eventName: "click",
      targetElement: "[data-tna-analytics-event='select_feature']",
      on: "click",
      data: {},
      rootEventName: "select_feature",
      rootData: {
        data_component_name: componentFromElement,
        data_section: ($el, $scope) =>
          $scope.dataset["tnaAnalyticsSection"] || null,
        data_link_type: linkTypeFromElement,
        data_link: helpers.valueGetters.text,
        data_label: ($el) => $el.dataset["tnaAnalyticsLabel"] || null,
        data_position: ($el, $scope, event, index) => index,
      },
    },
    {
      eventName: "click",
      targetElement: "[data-tna-analytics-event='select_cta']",
      on: "click",
      data: {},
      rootEventName: "select_cta",
      rootData: {
        data_component_name: componentFromElement,
        data_section: ($el, $scope) =>
          $scope.dataset["tnaAnalyticsSection"] || null,
        data_link_type: linkTypeFromElement,
        data_link: helpers.valueGetters.text,
        data_label: ($el) => $el.dataset["tnaAnalyticsLabel"] || null,
        data_position: ($el, $scope, event, index, instance) => instance,
      },
    },
  ]);
}
