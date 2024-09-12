console.log("Hey");

const exampleCallback = () => {
  console.log("Order complete!");
};

const iframeContainerId = "example-widget-trigger";
const $widgetContainer = document.getElementById(iframeContainerId);
const eventId = $widgetContainer?.dataset["eventid"];
if (eventId && window.EBWidgets) {
  window.EBWidgets.createWidget({
    widgetType: "checkout",
    eventId,
    iframeContainerId,
    iframeContainerHeight: 425,
    onOrderComplete: exampleCallback,
  });
}
