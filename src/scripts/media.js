import videojs from "video.js";
// import "videojs-youtube";
import "./lib/videojs-youtube-modified";

const cookies = window.TNAFrontendCookies;

let videoJsInstances = {};

if (cookies.isPolicyAccepted("marketing")) {
  document
    .querySelectorAll(
      '.etna-video--youtube[id][href^="https://www.youtube.com/watch?v="]',
    )
    .forEach(($video) => {
      const id = $video.getAttribute("id");
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
      $newVideo.setAttribute("id", id);
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
      videoJsInstances[id] = video;
    });
}

document.querySelectorAll(".etna-video--selfhosted[id]").forEach(($video) => {
  const id = $video.getAttribute("id");
  const video = videojs($video, {
    experimentalSvgIcons: true,
    enableSmoothSeeking: true,
    controlBar: {
      volumePanel: false,
    },
  });
  videoJsInstances[id] = video;
});

document.querySelectorAll(".etna-audio[id]").forEach(($audio) => {
  const id = $audio.getAttribute("id");
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
  videoJsInstances[id] = audio;
});

console.log(videoJsInstances);

Object.entries(videoJsInstances).forEach(([key, instance]) => {
  instance.on("play", () =>
    Object.entries(videoJsInstances).forEach(([key2, instance2]) =>
      key2 !== key ? instance2.pause() : null,
    ),
  );
});

document
  .querySelectorAll("button.media-chapter[value][aria-controls]")
  .forEach(($chapterButton) => {
    $chapterButton.addEventListener("click", () => {
      const id = $chapterButton.getAttribute("aria-controls");
      const time = $chapterButton.getAttribute("value");
      if (videoJsInstances[id]) {
        videoJsInstances[id].currentTime(time);
        videoJsInstances[id].play();
      } else {
        console.error(`Can't find ID ${id}`);
      }
    });
  });
