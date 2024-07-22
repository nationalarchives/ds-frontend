/* eslint-disable-next-line no-unused-vars */
const OFFLINE_VERSION = 1;
const CACHE_NAME = "offline";
const OFFLINE_URL = "/static/offline.html";

const contentToCache = [
  "/static/offline.css",
  "/static/offline.css.map",
  "/static/offline.min.js",
  "/static/offline.min.js.map",
  "/static/assets/fonts/OpenSans-Bold.ttf",
  "/static/assets/fonts/OpenSans-Regular.ttf",
  "/static/assets/images/favicon.ico",
  "/static/assets/images/tna-square-logo.svg",
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    (async () => {
      const cache = await caches.open(CACHE_NAME);
      // Setting {cache: 'reload'} in the new request will ensure that the response
      // isn't fulfilled from the HTTP cache; i.e., it will be from the network.
      await cache.add(new Request(OFFLINE_URL, { cache: "reload" }));
    })(),
  );
  event.waitUntil(
    (async () => {
      const cache = await caches.open(CACHE_NAME);
      await cache.addAll(contentToCache);
    })(),
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    (async () => {
      // Enable navigation preload if it's supported.
      // See https://developers.google.com/web/updates/2017/02/navigation-preload
      if ("navigationPreload" in self.registration) {
        await self.registration.navigationPreload.enable();
      }
    })(),
  );

  // Tell the active service worker to take control of the page immediately.
  self.clients.claim();
});

self.addEventListener("fetch", (event) => {
  // We only want to call event.respondWith() if this is a navigation request
  // for an HTML page.
  if (event.request.mode === "navigate") {
    event.respondWith(
      (async () => {
        try {
          // First, try to use the navigation preload response if it's supported.
          const preloadResponse = await event.preloadResponse;
          if (preloadResponse) {
            return preloadResponse;
          }

          const networkResponse = await fetch(event.request);
          return networkResponse;
        } catch (error) {
          // catch is only triggered if an exception is thrown, which is likely
          // due to a network error.
          // If fetch() returns a valid HTTP response with a response code in
          // the 4xx or 5xx range, the catch() will NOT be called.

          const cache = await caches.open(CACHE_NAME);
          const cachedResponse = await cache.match(OFFLINE_URL);
          return cachedResponse;
        }
      })(),
    );
  } else if (
    contentToCache.includes(
      `/static/${event.request.url.split("/static/").pop()}`,
    )
  ) {
    event.respondWith(
      (async () => {
        try {
          const preloadResponse = await event.preloadResponse;
          if (preloadResponse) {
            return preloadResponse;
          }

          const networkResponse = await fetch(event.request);
          return networkResponse;
        } catch (error) {
          const cache = await caches.open(CACHE_NAME);

          const cachedResource = await cache.match(event.request.url);
          if (cachedResource) {
            return cachedResource;
          }
        }
      })(),
    );
  }

  // If our if() condition is false, then this fetch handler won't intercept the
  // request. If there are any other fetch handlers registered, they will get a
  // chance to call event.respondWith(). If no fetch handlers call
  // event.respondWith(), the request will be handled by the browser as if there
  // were no service worker involvement.
});
