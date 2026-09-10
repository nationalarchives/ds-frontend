# Open Graph images

This service is capable of generating [Open Graph images](https://ogp.me/) using [Pillow](https://python-pillow.org/).

The code responsible can be found in `app/lib/og_images.py`.

## Wagtail content

For any Wagtail page (e.g. `/explore-the-collection/`) you can prefix the path with `/og` to render an OG image using the page's content.

- Page: https://localhost/explore-the-collection/
- Open Graph image: https://localhost/og/explore-the-collection/

All Wagtail pages have this integrated as part of the [meta tags template](./templates.md#meta).

### Supertitle

If set, the page's `type_label` is used.

### Title

In order of priority, the title is taken from one of these values:

1. `meta.seo_title`
1. `short_title`
1. `title` (a required field)

### Body

In order of priority, the body text is taken from one of these values:

1. `meta.search_description`
1. `meta.teaser_text` (a required field)

### Image

In order of priority, the image is taken from one of these values:

1. `meta.search_image.jpeg.full_url`
1. `meta.teaser_image.jpeg.full_url`
1. `hero_image.small_jpeg.full_url`
1. A default image (defined in the environment variable `OG_DEFAULT_IMAGE`)

## Pages from other services

If no Wagtail page exists for the requested OG image path, this service will attempt to scrape the desired path for content to build the image.

The domain used is set in the environment variable `OG_CONTENT_BASE_URL` and is set to a default of `https://www.nationalarchives.gov.uk`. This means the generator can only scrape pages on the main domain.

If you try to use `https://beta.nationalarchives.gov.uk/og/catalogue/`, the scraper will try `https://www.nationalarchives.gov.uk/catalogue/` for content.

To allow the scraper to find the required information, you should have at least the following meta tags in your page's `<head>`:

```html
<meta property="og:title" content="" />

<meta property="og:description" content="" />
<meta name="description" content="" />

<meta property="og:image" content="[your page's OG image path]" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta property="og:image:type" content="image/jpeg" />
```

### Supertitle

The scraper will try and capture the supertitle from the established markup for [headings with supertitles](https://design-system.nationalarchives.gov.uk/styles/typography/#headings-with-supertitles) for the `xl` and `<h1>` heading group.

### Title

In order of priority, the title is taken from one of these values:

1. The `content` of the `<meta property="og:title">` element
1. The `<h1>` element
1. The `<title>` element (removing the ` - The National Archives` suffix)

The title is then truncated to a length defined by the environment variable `OG_EXTERNAL_CONTENT_MAX_TITLE_LENGTH`. If longer than this, an elipsis is added at the end.

### Body

In order of priority, the body text is taken from one of these values:

1. The `content` of the `<meta property="og:description">` element
1. The `content` of the `<meta name="description">` element

The body text is then truncated to a length defined by the environment variable `OG_EXTERNAL_CONTENT_MAX_BODY_LENGTH`. If longer than this, an elipsis is added at the end.

### Image

A default image is used, defined by the environment variable `OG_DEFAULT_IMAGE`.
