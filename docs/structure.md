# Structure

## `app`

The application code.

### `app/feeds`

The routes for the blog feed page and the RSS and Atom XML files are defined here.

The templates for these routes can be found in `app/templates/blog`.

### `app/lib`

This contains reusable functionality that can be used throughout the site. Notable files are:

- `app/lib/api.py` - a generic JSON API client
- `app/lib/cache.py` - the cache configuration and cache keys
- `app/lib/content_parser.py` - functions to mutate content from Wagtail and transform it into TNA Frontend compilant code
- `app/lib/context_processor.py` - functions that can be used inside Jinja2 templates
- `app/lib/pagination.py` - create objects suitable for the pagination component in TNA Frontend
- `app/lib/talisman.py` - the reusable Talisman module for configuring security throughout the site
- `app/lib/template_filters.py` - filters that can be used in Jinja2 templates
- `app/lib/util.py` - replicates the `strtobool` function removed from Python 3.11

### `app/main`

The main routs for the site, including the healthcheck endpoint and static paths for `robots.txt` and `service-worker.min.js`.

### `app/search`

These routes are declared so we can construct URLs using the `url_for` function in this service but they should mirror the actual routes defined in the [`ds-sitemap-search` repository](https://github.com/nationalarchives/ds-sitemap-search/blob/main/app/sitemap_search/routes.py).

### `app/sitemaps`

Routes for creating the [XML sitemap](http://localhost:65535/sitemap.xml) and all the sub-sitemaps, e.g. [/sitemaps/sitemap_1.xml](http://localhost:65535/sitemaps/sitemap_1.xml), [/sitemaps/sitemap_2.xml](http://localhost:65535/sitemaps/sitemap_2.xml).

`/sitemap.xml` is the entrypoint sitemap that links to the other sitemaps.

`/sitemaps/sitemap_1.xml` is the sitemap that covers static routes defined in this service.

`/sitemaps/sitemap_2.xml` and onwards are dynamic pages defined in Wagtail.

The templates for these routes can be found in `app/templates/sitemaps`.

### `app/static`

This is largely ignored by version control as most of the static assets are compiled or copied in as part of the [`tna-build`](https://github.com/nationalarchives/docker/tree/main/docker/tna-python#tna-build) process in the `Dockerfile`.

Any static images that are needed for this site can be placed in `app/static/images` (which is not ignored by version control) and included in the HTML using the `url_for` function:

```
<img
    src="{{ url_for('static', filename='images/blank-profile.svg') }}"
    width="128"
    height="128"
    alt=""
>
```

Avoid adding large images and binary files to this repository. Try to use SVGs where possible

### `app/templates`

Jinja2 templates for the site.

Notable directories are:

- `app/templates/blog` - the blog pages and XML for the RSS and Atom feeds
- `app/templates/components` - duplicates of [TNA Frontend Jinja](https://github.com/nationalarchives/tna-frontend-jinja) templates which will override the default templates
- `app/templates/errors` - error pages such as 404 and 500 responses as well as the password protected template for private Wagtail pages
- `app/templates/explore-the-collection` - templates pertaining to `/explore-the-collection` routes in Wagtail
- `app/templates/layouts` - generic, reusable page layouts
- `app/templates/macros` - reusable macros, including the blocks that are used in Wagtail
- `app/templates/main` - page templates for the hub and general pages as well as one-time pages such as the cookies page and the home page
- `app/templates/people` - people index and person profile pages
- `app/templates/sitemaps` - the XML sitemap templates

### `app/wagtail`

Includes the routing for Wagtail pages and an API (`api.py`) to get content from Wagtail.

The routing will call `render_content_page` in `render.py` and depending on the page type from Wagtail (defined in `page_type_templates`) will load the appropriate page renderer from `app/wagtail/pages`.

## `src`

The source files for CSS and JavaScript.

### `src/scripts`

The JavaScript files to be compiled at build time.

Each file requiring compilation needs to be included in `webpack.config.js`.

JavaScript files get compiled to `app/static` and can be used in the templates with:

```html
{% block bodyEnd %} {{ super() }}
<script
  src="{{ url_for('static', filename='my-js-file.min.js', v=app_config.BUILD_VERSION) }}"
  defer
></script>
{% endblock %}
```

### `src/styles`

The SCSS files to be compiled to CSS at build time.

All SCSS files in this directory will be compiled to `app/static`. To exclude files from being compiled (such as modules for includes), prefix the files with an underscore (e.g. `src/styles/main/_generics.scss`).

These CSS files can be used in your templates with:

```html
{% block stylesheets %} {{ super() }}
<link
  rel="stylesheet"
  href="{{ url_for('static', filename='my-css-file.css', v=app_config.BUILD_VERSION) }}"
  media="screen,print"
/>
{% endblock %}
```

## `test`

Test files which should closely match the directory structure of the `app` directory.

## `.env`

Use an `.env` file to include API keys and other private environment variables that we don't want to commit to version control.

When you change calues in this file, you need to rebuild the containers with `docker compose up -d`.

## `.nvmrc`

The version of NodeJS that the container will use to build assets. Try to use the latest [LTS version of NodeJS](https://nodejs.org/en/about/previous-releases).

## `config.py`

A file containing configuration for `Production`, `Staging`, `Develop` and `Test`.

Define default values in `Base` and overwrite them only in the configurations that need it.

This is the applciation configuration and not the [container environment](https://github.com/nationalarchives/docker/tree/main/docker/tna-python#environment-variables) which affects how the code is run (number of threads/workers etc.).

## `docker-compose.yml`

This is only used for local development. Configuration added and edited here will not affect production builds.

Don't put secrets in here (e.g. API keys) - add these to an [`.env`](#env) file instead.

## `Dockerfile`

The file that will be used to build images in GitHub Actions.

Keep this file as terse as possible.

## `ds-frontend.py`

The entrypoint for the application as defined in the `tna-run` command on the [`Dockerfile`](#dockerfile).
