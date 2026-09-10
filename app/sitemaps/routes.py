import math
from urllib.parse import urlparse

from flask import (
    current_app,
    make_response,
    redirect,
    render_template,
    url_for,
)
from tna_utilities.datetime import get_date_from_string
from tna_utilities.flask import cacheable_duration

from app.error_pages.routes import page_not_found_error
from app.sitemaps import bp
from app.wagtail.api import all_pages_sitemap


@bp.route("/sitemap.xml")
@cacheable_duration(259200)
def sitemap_index():
    sitemap_urls = []
    wagtail_pages = all_pages_sitemap(page=1, limit=1)
    wagtail_pages_count = wagtail_pages["meta"]["total_count"]
    items_per_sitemap = current_app.config.get(
        "ITEMS_PER_SITEMAP", current_app.config["WAGTAILAPI_LIMIT_MAX"]
    )
    pages = math.ceil(wagtail_pages_count / items_per_sitemap)
    for page in range(1, pages + 1):
        sitemap_urls.append(
            url_for(
                "sitemaps.sitemap_dynamic",
                sitemap_page=page,
                _external=True,
                _scheme="https",
            )
        )
    xml_sitemap_index = render_template(
        "sitemaps/sitemaps_index.xml",
        sitemap_urls=sitemap_urls,
    )
    response = make_response(xml_sitemap_index)
    response.headers["Content-Type"] = "application/xml; charset=utf-8"
    return response


@bp.route("/sitemaps/")
def sitemaps():
    return redirect(
        url_for("sitemaps.sitemap_index"),
        code=301,
    )


@bp.route("/sitemaps/sitemap_<int:sitemap_page>.xml")
@cacheable_duration(86400)
def sitemap_dynamic(sitemap_page):
    exclude_urls = [
        "/maintenance/",
        "/education/",  # TODO: Remove this when the education section is live
    ]
    dynamic_urls = []
    items_per_sitemap = current_app.config.get(
        "ITEMS_PER_SITEMAP", current_app.config["WAGTAILAPI_LIMIT_MAX"]
    )
    wagtail_pages = all_pages_sitemap(
        page=sitemap_page,
        limit=items_per_sitemap,
    )
    wagtail_pages_count = wagtail_pages["meta"]["total_count"]
    pages = math.ceil(wagtail_pages_count / items_per_sitemap)
    if sitemap_page > pages:
        return page_not_found_error()
    for page in wagtail_pages["items"]:
        page_path = urlparse(page.get("full_url", "")).path
        if page_path.startswith(tuple(exclude_urls)):
            continue
        try:
            lastmodified_date = get_date_from_string(page["last_published_at"])
            lastmodified_date = lastmodified_date.strftime("%Y-%m-%d")
        except ValueError:
            current_app.logger.exception(
                f"Error parsing last_published_at for {page_path}"
            )
            lastmodified_date = None
        url = {
            "loc": page["full_url"],
            "lastmod": lastmodified_date,
        }
        dynamic_urls.append(url)
    xml_sitemap = render_template(
        "sitemaps/sitemap.xml",
        urls=dynamic_urls,
    )
    response = make_response(xml_sitemap)
    response.headers["Content-Type"] = "application/xml; charset=utf-8"
    return response
