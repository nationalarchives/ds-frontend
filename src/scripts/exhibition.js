// import { Cookies } from "@nationalarchives/frontend/nationalarchives/all.mjs";

// const cookies = new Cookies();

// const enhanceMaps = () =>
//   document.querySelectorAll("[data-mapembedurl]").forEach(($mapReplacement) => {
//     const $mapIframe = document.createElement("iframe");
//     $mapIframe.classList.add("tna-enhanced-map");
//     $mapIframe.setAttribute("tabindex", "0");
//     $mapIframe.setAttribute("src", $mapReplacement.dataset["mapembedurl"]);
//     $mapReplacement.replaceWith($mapIframe);
//     const mapLink = $mapReplacement.dataset["maplink"];
//     if (mapLink) {
//       const $mapLink = document.createElement("p");
//       $mapLink.classList.add("tna-!--margin-top-xs");
//       $mapLink.innerHTML = `<a href="${mapLink}">See full map</a>`;
//       $mapIframe.after($mapLink);
//     }
//   });

// if (cookies.preference("usage")) {
//   enhanceMaps();
// } else {
//   cookies.once("changePreference", (policies) => {
//     if (policies["usage"]) {
//       enhanceMaps();
//     }
//   });
// }
