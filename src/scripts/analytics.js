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
  ]);
}
