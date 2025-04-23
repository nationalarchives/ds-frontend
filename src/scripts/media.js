import videojs from "video.js";
// import "videojs-youtube";
import { initYoutubeEmbedApi } from "./lib/videojs-youtube-modified";

const cookies = window.TNAFrontendCookies;

let videoJsInstances = {};

const $youTubeVideoInstances = document.querySelectorAll(
  "a.etna-video--youtube[id]",
);

const updateYoutubeVideoMessages = ($youTubeVideoInstances) => {
  $youTubeVideoInstances.forEach(($video) => {
    $video.querySelector(".etna-video__label-cookies-message-js")?.remove();
  });
};

const initYouTubeVideos = ($youTubeVideoInstances) => {
  $youTubeVideoInstances.forEach(($video) => {
    const id = $video.getAttribute("id");
    const $newVideo = document.createElement("video");
    $newVideo.classList.add(
      "etna-video",
      "etna-video--youtube",
      "video-js",
      "vjs-16-9",
    );
    $newVideo.setAttribute("controls", true);
    $newVideo.setAttribute("id", id);
    const poster =
      $video
        .querySelector("img.etna-video__preview-image[src]")
        ?.getAttribute("src") || null;
    $video.replaceWith($newVideo);
    const video = videojs(
      $newVideo,
      {
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
        poster,
        youtube: {
          ytControls: 0,
          color: "white",
          enablePrivacyEnhancedMode: true,
          iv_load_policy: 3,
          rel: 0,
        },
      },
      () => {
        video.el().querySelector("iframe")?.setAttribute("tabindex", "-1");
      },
    );
    video.one("play", (player) =>
      player.target.querySelector("iframe")?.removeAttribute("tabindex"),
    );
    videoJsInstances[id] = video;
  });
};

if (cookies.isPolicyAccepted("marketing")) {
  initYoutubeEmbedApi(() => initYouTubeVideos($youTubeVideoInstances));
} else {
  cookies.once("changePolicy", (policies) => {
    if (policies["marketing"]) {
      initYoutubeEmbedApi(() => initYouTubeVideos($youTubeVideoInstances));
    }
  });
  updateYoutubeVideoMessages($youTubeVideoInstances);
}

document.querySelectorAll(".etna-video--selfhosted[id]").forEach(($video) => {
  const id = $video.getAttribute("id");
  const poster = $video.dataset.poster || null;
  const video = videojs($video, {
    experimentalSvgIcons: true,
    enableSmoothSeeking: true,
    textTrackSettings: false,
    controlBar: {
      volumePanel: false,
    },
    poster,
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
    $chapterButton.removeAttribute("hidden");
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

document
  .querySelectorAll(".media-chapter-heading")
  .forEach(($chapterHeading) => {
    $chapterHeading.setAttribute("hidden", "");
  });
