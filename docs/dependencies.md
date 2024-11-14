# Dependencies

Few dependencies have been used in order to keep the site more performant and secure.

## Poetry

- `flask-caching` - allows the cachine of routes and time-intensive functions
- `tna-frontend-jinja` - Jinja2 templates for TNA Frontend components
- `flask-talisman` - adds configuration for better security including [CSP](https://nationalarchives.github.io/engineering-handbook/technology/standards/security/#csp)
- `sentry-sdk` - sends Python errors to the Sentry dashboard for monitoring
- `pydash` - library of Python utilities to make object querying and manipulation easier

## npm

- `@sentry/browser` - allows errors in the frontend to be sent to the Sentry dashboard
- `video.js` - a video player to enhance plain `<video>` elements
- `videojs-youtube` - a plugin for video.js which allows a custom player for YouTube videos
