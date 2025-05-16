import {
  EventTracker,
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

class Matomo extends EventTracker {
  /** @protected */
  trackingEnabled = false;

  /** @protected */
  matomoUrl;

  /** @protected */
  matomoSiteId;

  /** @protected */
  matomoSiteDomain;

  constructor(options = {}) {
    if (window.TNAFrontendAnalyticsMatomo) {
      return window.TNAFrontendAnalyticsMatomo;
    }
    const {
      id = "",
      prefix = null,
      initAll = true,
      domain = "",
      url = "",
    } = options;
    super({ prefix });
    window.TNAFrontendAnalyticsMatomo = this;
    this.matomoUrl = url.replace(/\/$/, "");
    this.matomoSiteId = id;
    this.matomoSiteDomain = domain;
    window._paq = window._paq || [];
    this.start(initAll);
  }

  start(initAll) {
    if (!this.matomoSiteId) {
      throw Error("ID was not specified");
    }
    if (!this.matomoSiteDomain) {
      throw Error("Domain was not specified");
    }
    this.pushToPaq(["requireCookieConsent"]);
    this.pushToPaq(["setCookieDomain", this.matomoSiteDomain]);
    this.pushToPaq(["setDomains", [this.matomoSiteDomain]]);
    this.pushToPaq(["setDoNotTrack", true]);
    this.pushToPaq(["setTrackerUrl", `${this.matomoUrl}/matomo.php`]);
    this.pushToPaq(["setSiteId", this.matomoSiteId]);

    if (!navigator.doNotTrack || navigator.doNotTrack !== 1) {
      if (this.cookies.isPolicyAccepted("usage")) {
        this.enableTracking();
      }
      this.cookies.on("changePolicy", (policies) => {
        if (Object.hasOwn(policies, "usage")) {
          if (policies["usage"]) {
            this.enableTracking();
          } else {
            this.disableTracking();
          }
        }
      });
      if (initAll) {
        this.initAll();
      }
    }

    // TODO
    // this.pushToPaq({
    //   ...this.getTnaMetaTags(),
    //   ...this.getUserPreferences(),
    // });
  }

  destroy() {
    window.TNAFrontendAnalyticsMatomo = null;
  }

  /** @protected */
  recordEvent(eventName, data, rootData = {}) {
    console.log("Matomo event", eventName, data, rootData);
    // this.pushToPaq([
    //   "trackEvent",
    //   data.areaName,
    //   data.name,
    //   data.value,
    //   data.state || data.index /*, {dimension1: 'DimensionValue'}*/,
    // ]);
    this.pushToPaq([
      "trackContentInteraction",
      data.name,
      data.areaName,
      data.instance,
      data.value,
    ]);
  }

  /** @protected */
  pushToPaq(data) {
    console.log("Matomo pushToPaq", data);
    window._paq.push(data);
  }

  /** @protected */
  enableTracking() {
    this.pushToPaq(["setCookieConsentGiven"]);

    this.pushToPaq(["trackPageView"]);
    this.pushToPaq(["trackAllContentImpressions"]);
    this.pushToPaq(["enableLinkTracking"]);

    const firstScript = document.getElementsByTagName("script")[0];
    const script = document.createElement("script");
    script.async = true;
    script.src = `${this.matomoUrl}/matomo.js`;
    if (firstScript) {
      firstScript.parentNode.insertBefore(script, firstScript);
    } else {
      document.head.appendChild(script);
    }
  }

  /** @protected */
  disableTracking() {
    this.pushToPaq(["forgetCookieConsentGiven"]);
    this.pushToPaq(["optUserOut"]);
  }
}

new Matomo({
  url: document.documentElement.dataset.matomoUrl,
  id: document.documentElement.dataset.matomoSiteId,
  domain: document.documentElement.dataset.tnaCookiesDomain,
});
