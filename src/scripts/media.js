import Plyr from "plyr";

const cookies = window.TNAFrontendCookies;

if (cookies.isPolicyAccepted("marketing")) {
  document
    .querySelectorAll(
      '.etna-video--youtube:has([data-plyr-provider="youtube"][data-plyr-embed-id])',
    )
    .forEach(($video) => {
      const $nextButtonGroup = $video.nextElementSibling;
      if ($nextButtonGroup.classList.contains("tna-button-group")) {
        $nextButtonGroup.removeAttribute("hidden");
      }
      const iconUrl = $video.dataset["plyrSvg"] || null;
      const $videoEl = $video.querySelector(
        '[data-plyr-provider="youtube"][data-plyr-embed-id]',
      );
      $video.replaceWith($videoEl);
      new Plyr($videoEl, {
        iconUrl,
        youtube: { noCookie: true },
      });
    });
}

document.querySelectorAll(".etna-audio").forEach(($audio) => {
  new Plyr($audio, {
    iconUrl: $audio.dataset["plyrSvg"] || null,
  });
});

document.querySelectorAll(".etna-video--selfhosted").forEach(($video) => {
  new Plyr($video, {
    iconUrl: $video.dataset["plyrSvg"] || null,
  });
});
