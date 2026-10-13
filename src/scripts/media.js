import "@videojs/html/video/player";
import "@videojs/html/video/neutral-skin";

import "@videojs/html/audio/player";
import "@videojs/html/audio/neutral-skin";
import "@videojs/html/ui/poster";

// const videoJsInstances = {};

// document.querySelectorAll(".etna-video--selfhosted[id]").forEach(($video) => {
//   const id = $video.getAttribute("id");
//   const poster = $video.dataset.poster || null;
//   const video = videojs(
//     $video,
//     {
//       experimentalSvgIcons: true,
//       enableSmoothSeeking: true,
//       textTrackSettings: false,
//       controlBar: {
//         volumePanel: false,
//       },
//       poster,
//     },
//     () => {
//       video.el().removeAttribute("tabindex");
//       const videoTitle = video.el().dataset.title;
//       if (videoTitle) {
//         video.el().setAttribute("aria-label", `Video: ${videoTitle}`);
//       }
//     },
//   );
//   videoJsInstances[id] = video;
// });

// document.querySelectorAll(".etna-audio[id]").forEach(($audio) => {
//   const id = $audio.getAttribute("id");
//   const audio = videojs(
//     $audio,
//     {
//       audioOnlyMode: true,
//       enableSmoothSeeking: true,
//       experimentalSvgIcons: true,
//       controlBar: {
//         skipButtons: {
//           forward: 10,
//           backward: 10,
//         },
//         volumePanel: false,
//       },
//     },
//     () => {
//       audio.el().removeAttribute("tabindex");
//       const audioTitle = audio.el().dataset.title;
//       if (audioTitle) {
//         audio.el().setAttribute("aria-label", `Audio: ${audioTitle}`);
//       }
//     },
//   );
//   videoJsInstances[id] = audio;
// });

// Object.entries(videoJsInstances).forEach(([key, instance]) => {
//   instance.on("play", () => {
//     Object.entries(videoJsInstances).forEach(
//       ([key2, instance2]) => key2 !== key && instance2.pause(),
//     );
//   });
//   // instance.on("pause", () => {
//   //   instance.el().querySelector(".vjs-play-control")?.focus();
//   // });
// });

// document
//   .querySelectorAll("button.media-chapter[value][aria-controls]")
//   .forEach(($chapterButton) => {
//     $chapterButton.removeAttribute("hidden");
//     $chapterButton.addEventListener("click", () => {
//       const id = $chapterButton.getAttribute("aria-controls");
//       const time = $chapterButton.getAttribute("value");
//       if (videoJsInstances[id]) {
//         videoJsInstances[id].currentTime(time);
//         videoJsInstances[id].play();
//       }
//     });
//   });

// document
//   .querySelectorAll(".media-chapter-heading")
//   .forEach(($chapterHeading) => {
//     $chapterHeading.setAttribute("hidden", "");
//   });
