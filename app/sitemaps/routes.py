import math
from datetime import datetime
from urllib.parse import urlparse

from app.lib.cache import cache
from app.sitemaps import bp
from app.wagtail.api import all_pages
from flask import current_app, make_response, render_template, request, url_for


@bp.route("/sitemap.xml")
@cache.cached(timeout=3600)
def sitemaps():
    sitemap_urls = [
        url_for("sitemaps.sitemap_static", _external=True, _scheme="https")
    ]
    wagtail_pages = all_pages(limit=1)
    wagtail_pages_count = wagtail_pages["meta"]["total_count"]
    items_per_sitemap = current_app.config.get("ITEMS_PER_SITEMAP")
    pages = math.ceil(wagtail_pages_count / items_per_sitemap)
    for page in range(2, pages + 2):
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


def static_uris():
    static_uris = list()
    for rule in current_app.url_map.iter_rules():
        if (
            not str(rule).startswith("/preview")
            and not str(rule).startswith("/healthcheck")
            and not str(rule).startswith("/blog/feeds")
            and not str(rule).startswith("/sitemap.xml")
            and not str(rule).startswith("/robots.txt")
            and not str(rule).startswith("/sitemaps")
            and not str(rule).startswith("/service-worker.min.js")
        ):
            if "GET" in rule.methods and len(rule.arguments) == 0:
                static_uris.append(str(rule))
    return static_uris


@bp.route("/sitemaps/sitemap_1.xml")
@cache.cached(timeout=3600)
def sitemap_static():
    host_components = urlparse(request.host_url)
    host_base = "https://" + host_components.netloc
    static_urls = list()
    for uri in static_uris():
        url = {"loc": f"{host_base}{uri}"}
        static_urls.append(url)
    xml_sitemap = render_template(
        "sitemaps/sitemap.xml",
        urls=static_urls,
    )
    response = make_response(xml_sitemap)
    response.headers["Content-Type"] = "application/xml; charset=utf-8"
    return response


@bp.route("/sitemaps/sitemap_<int:sitemap_page>.xml")
@cache.cached(timeout=3600)
def sitemap_dynamic(sitemap_page):
    sitemap_page = sitemap_page - 1
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
        return render_template("errors/page-not-found.html"), 404
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
