import { initAll } from "@nationalarchives/frontend/nationalarchives/all.mjs";
// import {GA4} from "@nationalarchives/frontend/nationalarchives/analytics.mjs";
import "./modules/theme-switcher";

initAll();

/*
 * ==========================================
 * TEMP: ANALYTICS
 * ==========================================
 */
const TNAAnalytics = window.TNAFrontendAnalytics;
const ga4Id = document.documentElement.getAttribute("data-ga4id");
if (TNAAnalytics && ga4Id) {
  const analytics = new TNAAnalytics.GA4(ga4Id);

  analytics.addListener(".etna-article__sidebar", "sidebar", [
    {
      eventName: "scection_jump",
      targetElement: ".etna-article__sidebar-item",
      on: "click",
      data: {
        value: TNAAnalytics.helpers.valueGetters.text,
      },
    },
  ]);

  analytics.addListener(".etna-article", "article", [
    {
      eventName: "toggle_section",
      targetElement: ".etna-article__section-button",
      on: "click",
      data: {
        // eslint-disable-next-line no-unused-vars
        state: ($el, $scope, event) => {
          const expanded = $el.getAttribute("aria-expanded");
          if (expanded === null) {
            return null;
          }
          return expanded.toString() === "true" ? "opened" : "closed";
        },
        value: TNAAnalytics.helpers.valueGetters.text,
      },
    },
  ]);

  analytics.addListener(document.documentElement, "doc", [
    {
      eventName: "double_click",
      on: "dblclick",
      data: {
        state: ($el, $scope, event) => TNAAnalytics.getXPathTo(event.target),
        value: ($el, $scope, event) => event.target.innerHTML,
      },
    },
  ]);
}
