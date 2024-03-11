import { initAll } from "@nationalarchives/frontend/nationalarchives/all.mjs";
import {
  GA4,
  helpers,
} from "@nationalarchives/frontend/nationalarchives/analytics.mjs";
// import {
//      GA4,
//      helpers,
//    } from "./tmp/analytics.mjs";
import "./modules/theme-switcher";

initAll();

// const GA4 = window.TNAFrontendAnalytics.GA4;
// const helpers = window.TNAFrontendAnalytics.helpers;

const ga4Id = document.documentElement.getAttribute("data-ga4id");
if (ga4Id) {
  const analytics = new GA4(ga4Id);

  analytics.addListener(".etna-article__sidebar", "sidebar", [
    {
      eventName: "section.jump_to",
      targetElement: ".etna-article__sidebar-item",
      on: "click",
      data: {
        value: helpers.valueGetters.text,
      },
    },
  ]);

  analytics.addListener(".etna-article", "article", [
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

  analytics.addListener(document.documentElement, "doc", [
    {
      eventName: "double_click",
      on: "dblclick",
      data: {
        // eslint-disable-next-line no-unused-vars
        state: ($el, $scope, event, index) => helpers.getXPathTo(event.target),
        // eslint-disable-next-line no-unused-vars
        value: ($el, $scope, event, index) => event.target.innerHTML,
      },
    },
  ]);
}
