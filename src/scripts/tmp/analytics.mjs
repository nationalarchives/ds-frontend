import Cookies from "@nationalarchives/frontend/nationalarchives/lib/cookies.mjs";

const getXPathTo = ($element) => {
  if ($element.id !== "") {
    return 'id("' + $element.id + '")';
  }
  if ($element === document.body) {
    return $element.tagName;
  }
  let ix = 0;
  const siblings = $element.parentNode.childNodes;
  for (let i = 0; i < siblings.length; i++) {
    const sibling = siblings[i];
    if (sibling === $element)
      return (
        getXPathTo($element.parentNode) +
        "/" +
        $element.tagName +
        "[" +
        (ix + 1) +
        "]"
      );
    if (sibling.nodeType === 1 && sibling.tagName === $element.tagName) ix++;
  }
};

const includesAny = (arr, values) => values.some((v) => arr.includes(v));

const getClosestHeading = ($element) => {
  let heading = "";
  let $search = $element;
  do {
    while ($search.previousElementSibling) {
      $search = $search.previousElementSibling;
      if (
        ["h1", "h2", "h3", "h4", "h5", "h6"].includes($search.tagName) ||
        ($search.classList.length &&
          includesAny(Array.from($search.classList), [
            "tna-heading-xl",
            "tna-heading-l",
            "tna-heading-m",
            "tna-heading-s",
          ]))
      ) {
        heading = $search.innerText;
        break;
      }
    }
    $search = $search.parentElement;
  } while ($search.parentElement && !heading);
  return heading;
};

const valueGetters = {
  text: ($el) => $el.innerText,
  html: ($el) => $el.innerHTML,
  value: ($el) => $el.value,
  index: ($el, $scope, event, index) => index,
  checked: ($el) => ($el.checked ? "checked" : "unchecked"),
  expanded: ($el) => {
    const expanded = $el.getAttribute("aria-expanded");
    if (expanded === null) {
      return null;
    }
    return expanded.toString() === "true" ? "opened" : "closed";
  },
  closestHeading: ($el) => getClosestHeading($el),
};

const componentAnalytics = [
  {
    scope: ".tna-global-header",
    areaName: "header",
    events: [
      {
        eventName: "toggle",
        targetElement: ".tna-global-header__navigation-button",
        on: "click",
        data: {
          state: valueGetters.expanded,
        },
      },
      {
        eventName: "logo.click",
        targetElement: ".tna-global-header__logo",
        on: "click",
        rootData: {
          data_component_name: "Header",
          data_link_type: "Logo",
          data_link: "The National Archives",
        },
      },
      {
        eventName: "primary_link.click",
        targetElement: ".tna-global-header__navigation-item-link",
        on: "click",
        data: {
          value: valueGetters.text,
        },
        rootData: {
          data_component_name: "Header",
          data_link_type: "Menu",
          data_section: valueGetters.text,
          data_position: valueGetters.index,
          data_link: valueGetters.text,
        },
      },
      {
        eventName: "secondary_link.click",
        targetElement: ".tna-global-header__top-navigation-link",
        on: "click",
        data: {
          value: valueGetters.text,
        },
        rootData: {
          data_component_name: "Header",
          data_link_type: "Icon",
          data_position: valueGetters.index,
          data_link: valueGetters.text,
        },
      },
    ],
  },
  {
    scope: ".tna-footer",
    areaName: "footer",
    events: [
      {
        eventName: "link.click",
        targetElement: ".tna-footer__navigation-block-item-link",
        on: "click",
        data: {
          value: valueGetters.text,
        },
        rootData: {
          data_component_name: "Footer",
          data_link_type: "Link",
          data_section: valueGetters.closestHeading,
          data_position: valueGetters.index,
          data_link: valueGetters.text,
        },
      },
      {
        eventName: "social_link.click",
        targetElement: ".tna-footer__social-item-link",
        on: "click",
        data: {
          value: valueGetters.text,
        },
        rootData: {
          data_component_name: "Footer",
          data_link_type: "Icon",
          data_section: "Social media",
          data_position: valueGetters.index,
          data_link: ($el) => $el.getAttribute("data-name"),
        },
      },
      {
        eventName: "legal_link.click",
        targetElement: ".tna-footer__legal-item-link",
        on: "click",
        data: {
          value: valueGetters.text,
        },
        rootData: {
          data_component_name: "Footer",
          data_link_type: "Link",
          data_section: "Legal information",
          data_position: valueGetters.index,
          data_link: valueGetters.text,
        },
      },
      {
        eventName: "mailing_list.click",
        targetElement: ".tna-footer__mailing-list a.tna-button",
        on: "click",
        data: {
          value: valueGetters.text,
        },
        rootData: {
          data_component_name: "Footer",
          data_link_type: "Button",
          data_section: "Mailing list",
          data_link: valueGetters.text,
        },
      },
      {
        eventName: "ogl.click",
        targetElement: ".tna-footer__licence p a.tna-footer__link",
        on: "click",
        data: {
          value: valueGetters.text,
        },
        rootData: {
          data_component_name: "Footer",
          data_link_type: "Link",
          data_section: "OGL",
          data_link: valueGetters.text,
        },
      },
      {
        eventName: "govuk.click",
        targetElement: ".tna-footer__govuk-link",
        on: "click",
        data: {
          value: valueGetters.text,
        },
        rootData: {
          data_component_name: "Footer",
          data_link_type: "Logo",
          data_section: "GOV.UK",
          data_link: valueGetters.text,
        },
      },
    ],
  },
];

class EventTracker {
  /** @protected */
  cookies = new (window.TNAFrontend?.Cookies || Cookies)();

  /** @protected */
  events = [];

  /** @protected */
  start = new Date();

  /** @protected */
  prefix = "tna";

  constructor(prefix) {
    if (prefix) {
      this.prefix = prefix;
    }
  }

  /**
   * Initialise all TNA Frontend component analytics.
   */
  initAll() {
    componentAnalytics.forEach((componentConfig) => {
      this.addListener(
        componentConfig.scope,
        componentConfig.areaName,
        componentConfig.events,
      );
    });
  }

  /**
   * Add an event listener.
   * @param {String|HTMLElement} scope - The element to which the listener is scoped.
   * @param {String} areaName - The name of the component to pass on to the tracker.
   * @param {{eventName: String, targetElement: String|undefined, on: String, data: {value: Function|String|undefined, state: Function|String|undefined, [String]: any}}[]} events - The configuration of events to track along with their optional value and state which can be computed.
   */
  addListener(scope, areaName, events) {
    let scopeArray;
    if (typeof scope === "string") {
      scopeArray = Array.from(document.querySelectorAll(scope));
    } else if (typeof scope === "object") {
      scopeArray = [scope];
    }
    if (!scopeArray) {
      return;
    }
    scopeArray.forEach(($scope) => {
      events.forEach((eventConfig) => {
        if (!eventConfig.on) {
          return;
        }
        if (eventConfig.targetElement) {
          Array.from(
            $scope.querySelectorAll(eventConfig.targetElement),
          ).forEach(($el, index) =>
            this.attachListener(
              $el,
              $scope,
              this.generateEventName(areaName, eventConfig),
              eventConfig,
              scope,
              areaName,
              index + 1,
            ),
          );
        } else {
          this.attachListener(
            $scope,
            $scope,
            this.generateEventName(areaName, eventConfig),
            eventConfig,
            scope,
            areaName,
            1,
          );
        }
      });
    });
  }

  /** @protected */
  generateEventName(areaName, eventConfig) {
    return `${this.prefix}.${areaName}.${eventConfig.eventName || eventConfig.on}`;
  }

  /** @protected */
  attachListener($el, $scope, eventName, eventConfig, scope, areaName, index) {
    const { on, data, targetElement, rootData = {} } = eventConfig;
    $el.addEventListener(on, (event) =>
      this.recordEvent(
        eventName,
        {
          ...data,
          value: this.computedValue(data.value, $el, $scope, event, index),
          state: this.computedValue(data.state, $el, $scope, event, index),
          group: this.computedValue(data.group, $el, $scope, event, index),
          xPath: getXPathTo($scope),
          targetElement: targetElement,
          // timestamp: new Date().toISOString(),
          // uri: window.location.pathname,
          timeSincePageLoad: new Date() - this.start,
          index,
          scope,
          areaName,
        },
        Object.fromEntries(
          Object.entries(rootData).map(([key, value]) => [
            key,
            this.computedValue(value, $el, $scope, event, index),
          ]),
        ),
      ),
    );
  }

  /** @protected */
  computedValue(value, $el, $scope, event, index) {
    return typeof value === "function"
      ? value.call(this, $el, $scope, event, index)
      : value || null;
  }

  /** @protected */
  recordEvent(eventName, data, rootData = {}) {
    this.events.push({
      event: eventName,
      [`${this.prefix}.event`]: data,
      ...rootData,
    });
  }

  /** @protected */
  getTnaMetaTags() {
    return Object.fromEntries(
      Array.from(
        document.head.querySelectorAll(
          `meta[name^='${this.prefix}.'][content]`,
        ),
      ).map(($metaEl) => [
        $metaEl.getAttribute("name"),
        $metaEl.getAttribute("content"),
      ]),
    );
  }
}

/**
 * Class to handle Google Analytics 4 reporting.
 * @class GA4
 * @extends EventTracker
 * @constructor
 * @public
 */
class GA4 extends EventTracker {
  trackingCodeAdded = false;
  trackingEnabled = false;
  gTagId;

  constructor(id = null, options = {}) {
    if (GA4._instance) {
      return GA4._instance;
    }
    if (!id) {
      throw Error("ID was not specified");
    }
    const { prefix = null, initAll = true } = options;
    super(prefix);
    GA4._instance = this;
    this.gTagId = id;
    window.dataLayer = window.dataLayer || [];
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

  /** @protected */
  recordEvent(eventName, data, rootData = {}) {
    const ga4Data = {
      event: eventName,
      ...Object.fromEntries(
        Object.entries(data).map(([key, value]) => [
          `${this.prefix}.event.${key}`,
          value,
        ]),
      ),
      ...rootData,
    };
    this.pushToDataLayer(ga4Data);
  }

  /** @protected */
  gtag() {
    this.pushToDataLayer(arguments);
  }

  /** @protected */
  pushToDataLayer(data) {
    window.dataLayer.push(data);
  }

  /** @protected */
  enableTracking() {
    if (!this.trackingEnabled) {
      window["ga-disable-GA_MEASUREMENT_ID"] = false;
      this.trackingEnabled = true;
      if (!this.trackingCodeAdded) {
        this.pushToDataLayer({
          "gtm.start": new Date().getTime(),
          event: "gtm.js",
        });
        const firstScript = document.getElementsByTagName("script")[0];
        const script = document.createElement("script");
        script.async = true;
        script.src = `https://www.googletagmanager.com/gtm.js?id=${this.gTagId}&l=dataLayer`;
        firstScript.parentNode.insertBefore(script, firstScript);
        this.trackingCodeAdded = true;
        this.pushToDataLayer(this.getTnaMetaTags());
      }
      this.gtag("set", { allow_google_signals: true });
    }
  }

  /** @protected */
  disableTracking() {
    if (this.trackingEnabled) {
      window["ga-disable-GA_MEASUREMENT_ID"] = true;
      this.gtag("set", { allow_google_signals: false });
      this.trackingEnabled = false;
    }
  }
}

const helpers = { getXPathTo, getClosestHeading, valueGetters };

export { EventTracker, GA4, helpers };
