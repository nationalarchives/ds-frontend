import {
  GA4,
  helpers,
} from "@nationalarchives/frontend/nationalarchives/analytics.mjs";

const ga4Id = document.documentElement.getAttribute("data-ga4id");
if (ga4Id) {
  const analytics = new GA4({ id: ga4Id });

  analytics.addListeners(".etna-article__sidebar", "sidebar", [
    {
      eventName: "section.jump_to",
      targetElement: ".etna-article__sidebar-item",
      on: "click",
      data: {
        value: helpers.valueGetters.text,
      },
    },
  ]);

  analytics.addListeners(".etna-article", "article", [
    {
      eventName: "section.toggle",
      targetElement: ".etna-article__section-button",
      on: "click",
      data: {
        state: helpers.valueGetters.expanded,
        value: helpers.valueGetters.text,
      },
    },
  ]);

  analytics.addListeners(document.documentElement, "document", [
    {
      eventName: "double_click",
      on: "dblclick",
      data: {
        state: ($el, $scope, event) => helpers.getXPathTo(event.target),
      },
    },
  ]);
}
