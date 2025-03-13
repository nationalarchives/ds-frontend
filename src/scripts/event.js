const iframeContainerId = "example-widget-trigger";
const $widgetContainer = document.getElementById(iframeContainerId);
const eventId = $widgetContainer?.dataset["eventid"];
if (eventId && window.EBWidgets) {
  const exampleCallback = () => {
    console.log("Order complete!");
  };
  window.EBWidgets.createWidget({
    widgetType: "checkout",
    eventId,
    iframeContainerId,
    iframeContainerHeight: 600,
    onOrderComplete: exampleCallback,
  });
}
