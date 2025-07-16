# Templates

## Base templates

The base template `app/templates/base.html` extends `layouts/base.html` which is included in the [TNA Frontend Jinja package](https://github.com/nationalarchives/tna-frontend-jinja/blob/main/tna_frontend_jinja/templates/layouts/base.html).

The base page template adheres to the one described in the [page template description](https://nationalarchives.github.io/design-system/styles/page-template/) from the TNA Design System.

Set the `pageTitle` variable to change the content of the `<title>` element.

Ensure the page has a description and all the relevant elements to help with SEO.

## Templates for Wagtail pages

By default, we inject `page_data` into the Wagtail page templates. It includes everything that comes out of the `/pages/` API endpoint from Wagtail.

See an [example of the Wagtail API output](https://beta.nationalarchives.gov.uk/api/v2/pages/5/).

### Theme accent

Set `themeAccent` to one of the [available accent colours](https://nationalarchives.github.io/design-system/styles/colours/#accent-colours).

If there is a mourning notice, ensure the theme accent is set to `black`:

```
{% set themeAccent = 'black' if page_data.mourning_notice else 'pink' %}
```

### Meta

Pass the whole `page_data` from Wagtail (a repsonse from the `/pages/<int:page_id>/` endpoint) into the meta function from `macros/meta.html` to add all the relevant elements for SEO including OpenGraph tags:

```
{% block head %}
    {{ super() }}
    {{- meta(page_data) }}
{% endblock %}
```

### Global banners

Include the `global_alert_banners` function from `macros/global_alert_banners.html` and pass in the page's `global_alert` and `mourning_notice` properties to show the relevant notifications:

```
{{ global_alert_banners(page_data.global_alert, page_data.mourning_notice) }}
```
