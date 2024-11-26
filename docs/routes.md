# Routes

## Normal Wagtail page routing process

1. User requests URL (e.g. `https://www.nationalarchives.gov.uk/explore-the-collection/`)
1. Routes processed in `app/__init__.py`
1. Check for static routes first (`feeds`, `main`, `search`, `sitemaps`)
1. If no matching routes are found use the wagtail blueprint
1. Pass the path (e.g. `/explore-the-collection/`) into the `page` function in `app/wagtail/routes.py`
1. Pass the path to the API in order to find the page (`/api/v2/pages/find/?html_path=/explore-the-collection/`)
1. API redirects to page details (`/api/v2/pages/5/`)

## Page previews

The `preview_page` function in `app/wagtail/routes.py` responds to requests from Wagtail to preview pages in draft.

## Password protected pages

If the page returned from Wagtail is password protected, the request will be redirected to the `/preview/<int:page_id>/` path (handled by `preview_protected_page`) which will display a page for users to be able to enter a password in order to view the page.

## Permalinks

Because slugs and paths can change, each Wagtail page has a permalink in the format `/page/<int:page_id>/`, handled by `page_permalink`.

The permalink is referenced in the blog's RSS and Atom feeds.
