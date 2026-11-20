import { selectPlayback } from "@videojs/html";

import "@videojs/html/video/player";
// import "@videojs/html/video/skin";
import "@videojs/html/video/neutral-skin";
// import "@videojs/html/video/compat-skin";
// import "@videojs/html/video/scaffold-skin";

import "@videojs/html/audio/player";
// import "@videojs/html/audio/skin";
// import "@videojs/html/audio/neutral-skin";
import "@videojs/html/audio/compat-skin";
// import "@videojs/html/audio/scaffold-skin";

const players = Array.from(
  document.querySelectorAll("video-player, audio-player"),
  (player) => {
    player.querySelector("video")?.removeAttribute("controls");
    player.querySelector("audio")?.setAttribute("hidden", "");
    return player.store;
  },
);

players.forEach((player) => {
  let wasPaused = true;

  const syncPlayback = () => {
    const playback = selectPlayback(player.state);
    const startedPlaying = wasPaused && !playback.paused;
    wasPaused = playback.paused;

    if (startedPlaying) {
      players.forEach((otherPlayer) => {
        if (otherPlayer !== player) {
          const otherPlayback = selectPlayback(otherPlayer.state);
          if (!otherPlayback.paused || otherPlayback.autoplaying) {
            otherPlayback.pause();
          }
        }
      });
    }
  };

  player.subscribe(syncPlayback);
  syncPlayback();
});
