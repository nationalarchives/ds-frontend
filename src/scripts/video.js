import Plyr from "plyr";

const cookies = window.TNAFrontendCookies;

if (cookies.isPolicyAccepted("usage")) {
  const $youtubeVideos = document.querySelectorAll(
    '.etna-video:has([data-plyr-provider="youtube"][data-plyr-embed-id])',
  );

  $youtubeVideos.forEach(($video) => {
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
