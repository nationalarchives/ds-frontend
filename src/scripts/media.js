import videojs from "video.js";
// import "videojs-youtube";
import "./lib/videojs-youtube-modified";

const cookies = window.TNAFrontendCookies;

let videoJsInstances = [];

if (cookies.isPolicyAccepted("marketing")) {
  document
    .querySelectorAll(
      '.etna-video--youtube[href^="https://www.youtube.com/watch?v="]',
    )
    .forEach(($video) => {
      const $nextButtonGroup = $video.nextElementSibling;
      if ($nextButtonGroup.classList.contains("tna-button-group")) {
        $nextButtonGroup.removeAttribute("hidden");
      }
      const $newVideo = document.createElement("video");
      $newVideo.classList.add(
        "etna-video",
        "etna-video--youtube",
        "video-js",
        "vjs-16-9",
      );
      $newVideo.setAttribute("controls", true);
      $video.replaceWith($newVideo);
      const video = videojs($newVideo, {
        techOrder: ["youtube"],
        sources: [
          {
            type: "video/youtube",
            src: $video.getAttribute("href"),
          },
        ],
        experimentalSvgIcons: true,
        disablePictureInPicture: true,
        enableDocumentPictureInPicture: false,
        controlBar: {
          pictureInPictureToggle: false,
          volumePanel: false,
        },
        youtube: {
          ytControls: 0,
          color: "white",
          enablePrivacyEnhancedMode: true,
          iv_load_policy: 3,
          rel: 0,
        },
      });
      videoJsInstances.push(video);
    });
}

document.querySelectorAll(".etna-video--selfhosted").forEach(($video) => {
  const video = videojs($video, {
    experimentalSvgIcons: true,
    enableSmoothSeeking: true,
    controlBar: {
      volumePanel: false,
    },
  });
  videoJsInstances.push(video);
});

document.querySelectorAll(".etna-audio").forEach(($audio) => {
  const audio = videojs($audio, {
    audioOnlyMode: true,
    enableSmoothSeeking: true,
    experimentalSvgIcons: true,
    controlBar: {
      skipButtons: {
        forward: 10,
        backward: 10,
      },
      volumePanel: false,
    },
  });
  videoJsInstances.push(audio);
});

videoJsInstances.forEach((instance, index) => {
  instance.on("play", () =>
    videoJsInstances.forEach((instance2, index2) =>
      index2 !== index ? instance2.pause() : null,
    ),
  );
});
