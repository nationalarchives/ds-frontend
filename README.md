# nationalarchives.gov.uk Frontend

## Quickstart

```sh
# Build and start the container
docker compose up -d
```

### Add the static assets

During the first time install, your `app/static/assets` directory will be empty.

As you mount the project directory to the `/app` volume, the static assets from TNA Frontend installed inside the container will be "overwritten" by your empty directory.

To add back in the static assets, run:

```sh
docker compose exec app cp -r /app/node_modules/@nationalarchives/frontend/nationalarchives/assets /app/app/static
```

### Preview application

<http://localhost:65497/>

## Environment variables

In addition to the [base Docker image variables](https://github.com/nationalarchives/docker/blob/main/docker/tna-python/README.md#environment-variables), this application has support for:

| Variable                              | Purpose                                                                                     | Default                                              |
| ------------------------------------- | ------------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| `ENVIRONMENT_NAME`                    | The name of the environment (for reporting purposes)                                        | `production`                                         |
| `CONFIG`                              | The configuration to use                                                                    | `config.Production`                                  |
| `DEBUG`                               | If true, allow debugging[^1]                                                                | `False`                                              |
| `PROXY_DEPTH`                         | The number of proxies to trust for `X-Forwarded-` headers[^2]                               | `False`                                              |
| `SENTRY_DSN`                          | The Sentry DSN (project code)                                                               | _none_                                               |
| `SENTRY_JS_ID`                        | The ID of the Sentry client project to catch issues                                         | _none_                                               |
| `SENTRY_SAMPLE_RATE`                  | How often to sample traces and profiles (0-1.0)                                             | production: `0.1`, staging: `1`, develop: `0`        |
| `WAGTAIL_API_URL`                     | The base URL of the content API, including the `/api/v2` path                               | _none_                                               |
| `WAGTAIL_API_KEY`                     | A token used to access the Wagtail API                                                      | _none_                                               |
| `WAGTAIL_SITE_HOSTNAME`               | The site hostname in Wagtail, the default site is used if none is specified                 | _none_                                               |
| `WAGTAILAPI_LIMIT_MAX`                | The default maximum number of items to request from the Wagtail API                         | `20`                                                 |
| `ITEMS_PER_SITEMAP`                   | The maximum number of items to add to a single sitemap XML file                             | `500`                                                |
| `ITEMS_PER_BLOG_FEED`                 | The maximum number of items to add to a single RSS or Atom feed                             | `50`                                                 |
| `COOKIE_DOMAIN`                       | The domain to save cookie preferences against                                               | `.nationalarchives.gov.uk`                           |
| `COOKIE_PREFERENCES_URL`              | The URL for changing cookie preferences                                                     | `/cookies/`                                          |
| `COOKIE_PREFERENCES_SET_KEY`          | The cookie key specifying that the preferences have been set                                | `dontShowCookieNotice`                               |
| `CSP_IMG_SRC`                         | A comma separated list of CSP rules for `img-src`                                           | `'self'`                                             |
| `CSP_SCRIPT_SRC`                      | A comma separated list of CSP rules for `script-src`                                        | `'self'`                                             |
| `CSP_STYLE_SRC`                       | A comma separated list of CSP rules for `style-src`                                         | `'self'`                                             |
| `CSP_FONT_SRC`                        | A comma separated list of CSP rules for `font-src`                                          | `'self'`                                             |
| `CSP_CONNECT_SRC`                     | A comma separated list of CSP rules for `connect-src`                                       | `'self'`                                             |
| `CSP_MEDIA_SRC`                       | A comma separated list of CSP rules for `media-src`                                         | `'self'`                                             |
| `CSP_WORKER_SRC`                      | A comma separated list of CSP rules for `worker-src`                                        | `'self'`                                             |
| `CSP_FRAME_SRC`                       | A comma separated list of CSP rules for `frame-src`                                         | `'self'`                                             |
| `CSP_FRAME_ANCESTORS`                 | A domain from which to allow frame embedding (used in CMS previews)                         | _none_                                               |
| `CSP_REPORT_URL`                      | The URL to report CSP violations to                                                         | _none_                                               |
| `FORCE_HTTPS`                         | Redirect requests to HTTPS as part of the CSP                                               | _none_                                               |
| `PREFERRED_URL_SCHEME`                | Set the default protocol for generating links                                               | production/staging/develop: `https`, test: `http`    |
| `GA4_ID`                              | The Google Analytics 4 ID                                                                   | _none_                                               |
| `REDIRECT_WAGTAIL_ALIAS_PAGES`        | If true, redirect aliased Wagtail pages to the URI of their "original" page                 | `True`                                               |
| `SERVE_WAGTAIL_PAGE_REDIRECTIONS`     | If true, forward Wagtail page redirects to the user rather than proxying                    | `True`                                               |
| `SERVE_WAGTAIL_EXTERNAL_REDIRECTIONS` | If true, forward Wagtail redirects to external links                                        | `True`                                               |
| `FEATURE_LOGO_ADORNMENTS_CSS`         | An optional CSS file to include for logo adornments                                         | _none_                                               |
| `FEATURE_LOGO_ADORNMENTS_JS`          | An optional JS file to include for logo adornments                                          | _none_                                               |
| `WEBARCHIVE_BASE_URL`                 | The base URL of the web archive viewer                                                      | `https://webarchive.nationalarchives.gov.uk/ukgwa/+` |
| `WEBARCHIVE_CDXJ_API_URL`             | The base URL of the web archive CDXJ API                                                    | `https://webarchive.nationalarchives.gov.uk/ukgwa`   |
| `WEBARCHIVE_CDXJ_API_PATH`            | The path of the web archive CDXJ API                                                        | `cdx`                                                |
| `SIDEBAR_SCROLL_TOP_THRESHOLD`        | The distance from the top of the window before the sidebar section highlight is highlighted | `16`                                                 |

[^1] [Debugging in Flask](https://flask.palletsprojects.com/en/2.3.x/debugging/)
[^2] [Tell Flask it is Behind a Proxy](https://flask.palletsprojects.com/en/stable/deploying/proxy_fix/)

## Running tests

```sh
poetry run python -m pytest
```
