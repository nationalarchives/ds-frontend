# beta.nationalarchives.gov.uk frontend

## Quickstart

```sh
# Build and start the container
docker compose up -d

# Install Node modules
npm install

# Create a static assets directory
mkdir app/static/assets

# Copy in the static assets from TNA Frontend and Plyr
cp -r node_modules/@nationalarchives/frontend/nationalarchives/assets/* app/static/assets
```

## Environment variables

In addition to the [base Docker image variables](https://github.com/nationalarchives/docker/blob/main/docker/tna-python/README.md#environment-variables), this application has support for:

| Variable                         | Purpose                                                                     | Default                                                     |
| -------------------------------- | --------------------------------------------------------------------------- | ----------------------------------------------------------- |
| `CONFIG`                         | The configuration to use                                                    | `config.Production`                                         |
| `DEBUG`                          | If true, allow debugging[^1]                                                | `False`                                                     |
| `SENTRY_DSN`                     | The Sentry DSN (project code)                                               | _none_                                                      |
| `SENTRY_JS_ID`                   | The ID of the Sentry client project to catch issues                         | _none_                                                      |
| `SENTRY_SAMPLE_RATE`             | How often to sample traces and profiles (0-1.0)                             | production: `0.1`, staging: `0.25`, develop: `1`, test: `0` |
| `WAGTAIL_API_URL`                | The base URL of the content API, including the `/api/v2` path               | _none_                                                      |
| `WAGTAILAPI_LIMIT_MAX`           | The maximum number of items requested from the Wagtail API in one call      | `20`                                                        |
| `COOKIE_DOMAIN`                  | The domain to save cookie preferences against                               | _none_                                                      |
| `CSP_IMG_SRC`                    | A comma separated list of CSP rules for `img-src`                           | `'self'`                                                    |
| `CSP_SCRIPT_SRC`                 | A comma separated list of CSP rules for `script-src`                        | `'self'`                                                    |
| `CSP_SCRIPT_SRC_ELEM`            | A comma separated list of CSP rules for `script-src-elem`                   | `'self'`                                                    |
| `CSP_STYLE_SRC`                  | A comma separated list of CSP rules for `style-src`                         | `'self'`                                                    |
| `CSP_STYLE_SRC_ELEM`             | A comma separated list of CSP rules for `style-src-elem`                    | `'self'`                                                    |
| `CSP_FONT_SRC`                   | A comma separated list of CSP rules for `font-src`                          | `'self'`                                                    |
| `CSP_CONNECT_SRC`                | A comma separated list of CSP rules for `connect-src`                       | `'self'`                                                    |
| `CSP_MEDIA_SRC`                  | A comma separated list of CSP rules for `media-src`                         | `'self'`                                                    |
| `CSP_WORKER_SRC`                 | A comma separated list of CSP rules for `worker-src`                        | `'self'`                                                    |
| `CSP_FRAME_SRC`                  | A comma separated list of CSP rules for `frame-src`                         | `'self'`                                                    |
| `CSP_FEATURE_FULLSCREEN`         | A comma separated list of rules for the `fullscreen` feature policy         | `'self'`                                                    |
| `CSP_FEATURE_PICTURE_IN_PICTURE` | A comma separated list of rules for the `picture-in-picture` feature policy | `'self'`                                                    |
| `FRAME_DOMAIN_ALLOW`             | A domain from which to allow frame embedding (used in CMS previews)         | _none_                                                      |
| `FORCE_HTTPS`                    | Redirect requests to HTTPS as part of the CSP                               | _none_                                                      |
| `CACHE_TYPE`                     | https://flask-caching.readthedocs.io/en/latest/#configuring-flask-caching   | _none_                                                      |
| `CACHE_DEFAULT_TIMEOUT`          | The number of seconds to cache pages for                                    | production: `300`, staging: `60`, develop: `0`, test: `0`   |
| `CACHE_DIR`                      | Directory for storing cached responses when using `FileSystemCache`         | `/tmp`                                                      |
| `GA4_ID`                         | The Google Analytics 4 ID                                                   | _none_                                                      |
| `APPLY_REDIRECTS`                | If true, redirect pages based on Wagtail redirects (false just displays)    | production/staging/develop: `True`, test: `False`           |

[^1] [Debugging in Flask](https://flask.palletsprojects.com/en/2.3.x/debugging/)

## Running tests

```sh
poetry run python -m pytest
```
