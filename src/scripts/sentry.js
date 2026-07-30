import * as Sentry from "@sentry/browser";

if (document.currentScript?.dataset?.id) {
  let release = null;
  if (document.currentScript.dataset.version) {
    release = `ds-frontend@${document.currentScript.dataset.version}`;
  }
  Sentry.init({
    dsn: `https://${document.currentScript.dataset.id}@o1230303.ingest.us.sentry.io/4507458004910080`,
    environment: document.currentScript?.dataset?.environment || "production",
    release,
    integrations: [
      Sentry.browserTracingIntegration(),
      Sentry.replayIntegration(),
    ],
    sampleRate: document.currentScript?.dataset?.samplerate || 1.0,
    tracesSampleRate: document.currentScript?.dataset?.samplerate || 1.0,
    replaysSessionSampleRate: 0.1,
    replaysOnErrorSampleRate: 1.0,
  });
}
