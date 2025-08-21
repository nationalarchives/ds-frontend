import math
from datetime import datetime

from app.lib.cache import cache, path_cache_key_prefix
from app.sitemaps import bp
from app.wagtail.api import all_pages
from flask import (
    current_app,
    make_response,
    redirect,
    render_template,
    request,
    url_for,
)


@bp.route("/sitemap.xml")
@cache.cached(timeout=14400, key_prefix=path_cache_key_prefix)  # 4 hours
def sitemap_index():
    sitemap_urls = []
    wagtail_pages = all_pages(limit=1)
    wagtail_pages_count = wagtail_pages["meta"]["total_count"]
    items_per_sitemap = current_app.config.get("ITEMS_PER_SITEMAP")
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
@cache.cached(timeout=14400, key_prefix=path_cache_key_prefix)  # 4 hours
def sitemap_dynamic(sitemap_page):
    current_app.logger.info("=== Generating sitemap index ===")
    current_app.logger.info(f"HOST HEADER: {request.headers.get('Host')}")
    current_app.logger.info(f"ALL HEADERS: {request.headers}")
    current_app.logger.info(f"HOST:        {request.host}")
    current_app.logger.info(f"URL:         {request.url}")
    current_app.logger.info(f"FULL PATH:   {request.url}")
    dynamic_urls = list()
    items_per_sitemap = current_app.config.get("ITEMS_PER_SITEMAP")
    wagtail_pages = all_pages(
        batch=sitemap_page,
        limit=items_per_sitemap,
        params={"order": "id"},
    )
    wagtail_pages_count = wagtail_pages["meta"]["total_count"]
    pages = math.ceil(wagtail_pages_count / items_per_sitemap)
    if sitemap_page > pages:
        return render_template("errors/page_not_found.html"), 404
    for page in wagtail_pages["items"]:
        try:
            lastmodified_date = datetime.strptime(
                page["last_published_at"], "%Y-%m-%dT%H:%M:%S.%fZ"
            )
            lastmodified_date = lastmodified_date.strftime("%Y-%m-%d")
        except KeyError:
            lastmodified_date = None
        except ValueError:
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
