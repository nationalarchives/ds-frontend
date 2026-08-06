import Cookies from "@nationalarchives/cookies";
import videojs from "video.js";

// import "videojs-youtube";
import { initYoutubeEmbedApi } from "./lib/videojs-youtube-modified";

const cookies = new Cookies();
const videoJsInstances = {};
const $youTubeVideoInstances = document.querySelectorAll(
  "a.etna-video--youtube[id]",
);
const updateYoutubeVideoMessages = ($youTubeVideoInstancesToUpdate) => {
  $youTubeVideoInstancesToUpdate.forEach(($video) => {
    $video.querySelector(".etna-video__label-cookies-message-js")?.remove();
  });
};
/* eslint-disable-next-line max-lines-per-function */
const initYouTubeVideos = ($youTubeVideoInstancesToInit) => {
  /* eslint-disable-next-line max-lines-per-function, max-statements */
  $youTubeVideoInstancesToInit.forEach(($video) => {
    const id = $video.getAttribute("id");
    const videoTitle = $video.dataset.title || null;
    const $newVideo = document.createElement("video");
    $newVideo.classList.add("etna-video", "etna-video--youtube", "video-js");
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
          /* eslint-disable-next-line camelcase */
          iv_load_policy: 3,
          rel: 0,
        },
      },
      () => {
        video.el().querySelector("iframe")?.setAttribute("tabindex", "-1");
        video.el().removeAttribute("tabindex");
        if (videoTitle) {
          video.el().setAttribute("aria-label", `YouTube video: ${videoTitle}`);
        }
      },
    );
    video.one("play", (player) =>
      player.target.querySelector("iframe")?.removeAttribute("tabindex"),
    );
    videoJsInstances[id] = video;
  });
};

if (cookies.preference("marketing")) {
  initYoutubeEmbedApi(() => initYouTubeVideos($youTubeVideoInstances));
} else {
  cookies.once("changePreference", (policies) => {
    if (policies.marketing) {
      initYoutubeEmbedApi(() => initYouTubeVideos($youTubeVideoInstances));
    }
  });
  updateYoutubeVideoMessages($youTubeVideoInstances);
}

document.querySelectorAll(".etna-video--selfhosted[id]").forEach(($video) => {
  const id = $video.getAttribute("id");
  const poster = $video.dataset.poster || null;
  const video = videojs(
    $video,
    {
      experimentalSvgIcons: true,
      enableSmoothSeeking: true,
      textTrackSettings: false,
      controlBar: {
        volumePanel: false,
      },
      poster,
    },
    () => {
      video.el().removeAttribute("tabindex");
      const videoTitle = video.el().dataset.title;
      if (videoTitle) {
        video.el().setAttribute("aria-label", `Video: ${videoTitle}`);
      }
    },
  );
  videoJsInstances[id] = video;
});

document.querySelectorAll(".etna-audio[id]").forEach(($audio) => {
  const id = $audio.getAttribute("id");
  const audio = videojs(
    $audio,
    {
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
    },
    () => {
      audio.el().removeAttribute("tabindex");
      const audioTitle = audio.el().dataset.title;
      if (audioTitle) {
        audio.el().setAttribute("aria-label", `Audio: ${audioTitle}`);
      }
    },
  );
  videoJsInstances[id] = audio;
});

Object.entries(videoJsInstances).forEach(([key, instance]) => {
  instance.on("play", () => {
    Object.entries(videoJsInstances).forEach(
      ([key2, instance2]) => key2 !== key && instance2.pause(),
    );
  });
  // instance.on("pause", () => {
  //   instance.el().querySelector(".vjs-play-control")?.focus();
  // });
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
      }
    });
  });

document
  .querySelectorAll(".media-chapter-heading")
  .forEach(($chapterHeading) => {
    $chapterHeading.setAttribute("hidden", "");
  });
