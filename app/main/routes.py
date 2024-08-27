import json
from urllib.parse import quote, unquote, urlparse

from app.lib import cache, cache_key_prefix
from app.lib.util import strtobool
from app.main import bp
from app.wagtail.api import all_pages, global_alerts
from flask import (
    current_app,
    make_response,
    redirect,
    render_template,
    request,
    url_for,
)


@bp.route("/healthcheck/live/")
def healthcheck():
    return "ok"


@bp.route("/browse/")
# @cache.cached(key_prefix=cache_key_prefix)
def browse():
    return render_template("main/browse.html", global_alert=global_alerts())


@bp.route("/cookies/", methods=["GET", "POST"])
def cookies():
    if request.method == "POST":
        current_cookies_policy = {
            "usage": False,
            "settings": False,
            "marketing": False,
            "essential": True,
        }
        if "cookies_policy" in request.cookies:
            cookies_policy = request.cookies["cookies_policy"]
            current_cookies_policy = json.loads(unquote(cookies_policy))
        usage = (
            strtobool(request.form["usage"])
            if "usage" in request.form
            else current_cookies_policy["usage"]
        )
        settings = (
            strtobool(request.form["settings"])
            if "settings" in request.form
            else current_cookies_policy["settings"]
        )
        marketing = (
            strtobool(request.form["marketing"])
            if "marketing" in request.form
            else current_cookies_policy["marketing"]
        )
        new_cookies_policy = {
            "usage": usage,
            "settings": settings,
            "marketing": marketing,
            "essential": True,
        }
        response = make_response(
            redirect(
                url_for(
                    "main.cookies",
                    saved="true",
                    referrer=(
                        request.form["referrer"]
                        if "referrer" in request.form
                        else ""
                    ),
                )
            )
        )
        response.set_cookie(
            "cookies_policy",
            quote(json.dumps(new_cookies_policy, separators=(",", ":"))),
            domain=current_app.config.get("COOKIE_DOMAIN"),
        )
        response.set_cookie(
            "cookie_preferences_set",
            "true",
            domain=current_app.config.get("COOKIE_DOMAIN"),
        )
        if not usage:
            for cookie in request.cookies:
                if cookie.startswith("_ga"):
                    response.set_cookie(cookie, "", expires=0)
        return response
    global_alerts_data = global_alerts()
    return render_template(
        "main/cookies.html",
        page_data={
            "title": "Cookies",
            "intro": f"""<p>Cookies are files saved on your phone, tablet or computer when you visit a website.</p>
<p>We use cookies to collect and store information about how you use National Archives websites which means any page with nationalarchives.gov.uk in the URL.</p>
<p>This page has a brief explanation of each type of cookie we use. If you want more details, <a href="{url_for('main.cookie_details')}">our detailed cookie information</a>.</p>""",
            "global_alert": global_alerts_data["global_alert"],
            "mourning_notice": global_alerts_data["mourning_notice"],
        },
    )


@bp.route("/cookies/details/")
# @cache.cached(key_prefix=cache_key_prefix)
def cookie_details():
    return render_template(
        "main/cookie-details.html", global_alert=global_alerts()
    )


@bp.route("/service-worker.min.js")
def service_worker():
    return current_app.send_static_file("service-worker.min.js")


@bp.route("/robots.txt")
def robots():
    return current_app.send_static_file("robots.txt")


@bp.route("/sitemap.xml")
@cache.cached(timeout=3600)
def sitemap():
    host_components = urlparse(request.host_url)
    host_base = host_components.scheme + "://" + host_components.netloc
    static_urls = list()
    for rule in current_app.url_map.iter_rules():
        if (
            not str(rule).startswith("/preview")
            and not str(rule).startswith("/healthcheck")
            and not str(rule).startswith("/sitemap.xml")
            and not str(rule).startswith("/service-worker.min.js")
        ):
            if "GET" in rule.methods and len(rule.arguments) == 0:
                url = {"loc": f"{host_base}{str(rule)}"}
                static_urls.append(url)
    dynamic_urls = list()
    page_batch = 0
    wagtail_pages_count = 1
    wagtail_pages_added = 0
    while wagtail_pages_added < wagtail_pages_count:
        page_batch = page_batch + 1
        wagtail_pages = all_pages(batch=page_batch)
        wagtail_pages_count = wagtail_pages["meta"]["total_count"]
        for page in wagtail_pages["items"]:
            html_url = page["full_url"]
            if not any(
                static_url["loc"] == html_url for static_url in static_urls
            ):
                url = {
                    "loc": html_url,
                    # "lastmod": post.date_published.strftime("%Y-%m-%dT%H:%M:%SZ")
                }
                dynamic_urls.append(url)
        wagtail_pages_added = wagtail_pages_added + len(wagtail_pages["items"])
    xml_sitemap = render_template(
        "main/sitemap.xml",
        static_urls=static_urls,
        dynamic_urls=dynamic_urls,
        host_base=host_base,
    )
    response = make_response(xml_sitemap)
    response.headers["Content-Type"] = "application/xml"
    return response


@bp.route("/new-homepage/")
# @cache.cached(key_prefix=cache_key_prefix)
def new_homepage():
    return render_template("main/new_home.html")
