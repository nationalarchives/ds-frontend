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

<http://localhost:65535/>

## Environment variables

In addition to the [base Docker image variables](https://github.com/nationalarchives/docker/blob/main/docker/tna-python/README.md#environment-variables), this application has support for:

| Variable                              | Purpose                                                                     | Default                                        |
| ------------------------------------- | --------------------------------------------------------------------------- | ---------------------------------------------- |
| `ENVIRONMENT_NAME`                    | The name of the environment (for reporting purposes)                        | `production`                                   |
| `CONFIG`                              | The configuration to use                                                    | `config.Production`                            |
| `DEBUG`                               | If true, allow debugging[^1]                                                | `False`                                        |
| `SENTRY_DSN`                          | The Sentry DSN (project code)                                               | _none_                                         |
| `SENTRY_JS_ID`                        | The ID of the Sentry client project to catch issues                         | _none_                                         |
| `SENTRY_SAMPLE_RATE`                  | How often to sample traces and profiles (0-1.0)                             | production: `0.1`, staging: `1`, develop: `0`  |
| `WAGTAIL_API_URL`                     | The base URL of the content API, including the `/api/v2` path               | _none_                                         |
| `WAGTAILAPI_LIMIT_MAX`                | The default maximum number of items to request from the Wagtail API         | `20`                                           |
| `ITEMS_PER_SITEMAP`                   | The maximum number of items to add to a single sitemap XML file             | `500`                                          |
| `ITEMS_PER_BLOG_FEED`                 | The maximum number of items to add to a single RSS or Atom feed             | `50`                                           |
| `COOKIE_DOMAIN`                       | The domain to save cookie preferences against                               | _none_                                         |
| `CSP_IMG_SRC`                         | A comma separated list of CSP rules for `img-src`                           | `'self'`                                       |
| `CSP_SCRIPT_SRC`                      | A comma separated list of CSP rules for `script-src`                        | `'self'`                                       |
| `CSP_SCRIPT_SRC_ELEM`                 | A comma separated list of CSP rules for `script-src-elem`                   | `'self'`                                       |
| `CSP_STYLE_SRC`                       | A comma separated list of CSP rules for `style-src`                         | `'self'`                                       |
| `CSP_STYLE_SRC_ELEM`                  | A comma separated list of CSP rules for `style-src-elem`                    | `'self'`                                       |
| `CSP_FONT_SRC`                        | A comma separated list of CSP rules for `font-src`                          | `'self'`                                       |
| `CSP_CONNECT_SRC`                     | A comma separated list of CSP rules for `connect-src`                       | `'self'`                                       |
| `CSP_MEDIA_SRC`                       | A comma separated list of CSP rules for `media-src`                         | `'self'`                                       |
| `CSP_WORKER_SRC`                      | A comma separated list of CSP rules for `worker-src`                        | `'self'`                                       |
| `CSP_FRAME_SRC`                       | A comma separated list of CSP rules for `frame-src`                         | `'self'`                                       |
| `CSP_FEATURE_FULLSCREEN`              | A comma separated list of rules for the `fullscreen` feature policy         | `'self'`                                       |
| `CSP_FEATURE_PICTURE_IN_PICTURE`      | A comma separated list of rules for the `picture-in-picture` feature policy | `'self'`                                       |
| `CSP_FRAME_ANCESTORS`                 | A domain from which to allow frame embedding (used in CMS previews)         | _none_                                         |
| `FORCE_HTTPS`                         | Redirect requests to HTTPS as part of the CSP                               | _none_                                         |
| `PREFERRED_URL_SCHEME`                | Set the default protocol for generating links                               | production/staging: `https`, develop: `http`   |
| `CACHE_TYPE`                          | https://flask-caching.readthedocs.io/en/latest/#configuring-flask-caching   | `FileSystemCache`                              |
| `CACHE_DEFAULT_TIMEOUT`               | The number of seconds to cache pages for                                    | production: `300`, staging: `10`, develop: `1` |
| `CACHE_DIR`                           | Directory for cache when using `CACHE_TYPE=FileSystemCache`                 | `/tmp`                                         |
| `CACHE_REDIS_URL`                     | The connection string for Redis when using `CACHE_TYPE=RedisCache`          | _none_                                         |
| `GA4_ID`                              | The Google Analytics 4 ID                                                   | _none_                                         |
| `MATOMO_URL`                          | The base URL of the Matomo instance                                         | _none_                                         |
| `MATOMO_SITE_ID`                      | The Matomo site ID                                                          | _none_                                         |
| `REDIRECT_WAGTAIL_ALIAS_PAGES`        | If true, redirect aliased Wagtail pages to the URI of their "original" page | `True`                                         |
| `SERVE_WAGTAIL_PAGE_REDIRECTIONS`     | If true, forward Wagtail page redirects to the user rather than proxying    | `True`                                         |
| `SERVE_WAGTAIL_EXTERNAL_REDIRECTIONS` | If true, forward Wagtail redirects to external links                        | `True`                                         |
| `FEATURE_LOGO_ADORNMENTS_CSS`         | An optional CSS file to include for logo adornments                         | _none_                                         |
| `FEATURE_LOGO_ADORNMENTS_JS`          | An optional JS file to include for logo adornments                          | _none_                                         |

[^1] [Debugging in Flask](https://flask.palletsprojects.com/en/2.3.x/debugging/)

## Running tests

```sh
poetry run python -m pytest
```
