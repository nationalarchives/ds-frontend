import calendar
import json
from datetime import datetime
from urllib.parse import quote, unquote, urlparse

from app.lib import cache, cache_key_prefix
from app.lib.api import ApiResourceNotFound
from app.lib.util import strtobool
from app.main import bp
from app.wagtail.api import (
    all_pages,
    blog_posts_paginated,
    global_alerts,
    page_details,
    page_details_by_type,
)
from flask import (
    current_app,
    make_response,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_caching import CachedResponse


@bp.route("/healthcheck/live/")
def healthcheck():
    return "ok"


@bp.route("/browse/")
@cache.cached(key_prefix=cache_key_prefix)
def browse():
    return render_template("main/browse.html", global_alert=global_alerts())


@bp.route("/help/cookies/set/", methods=["POST"])
def set_cookies():
    current_cookies_policy = {
        "usage": False,
        "settings": False,
        "marketing": False,
        "essential": True,
    }
    if "cookies_policy" in request.cookies:
        current_cookies_policy = json.loads(
            unquote(request.cookies["cookies_policy"])
        )
    usage = (
        strtobool(request.form["usage"])
        if "usage" in request.form
        else bool(current_cookies_policy["usage"])
    )
    settings = (
        strtobool(request.form["settings"])
        if "settings" in request.form
        else bool(current_cookies_policy["settings"])
    )
    marketing = (
        strtobool(request.form["marketing"])
        if "marketing" in request.form
        else bool(current_cookies_policy["marketing"])
    )
    new_cookies_policy = {
        "usage": usage,
        "settings": settings,
        "marketing": marketing,
        "essential": True,
    }
    response = make_response(redirect(f"{request.form['referrer']}?saved=true"))
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
    host_base = "https://" + host_components.netloc
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
                if url not in static_urls:
                    dynamic_urls.append(url)
        wagtail_pages_added = wagtail_pages_added + len(wagtail_pages["items"])
    xml_sitemap = render_template(
        "main/sitemap.xml",
        static_urls=static_urls,
        dynamic_urls=dynamic_urls,
        host_base=host_base,
    )
    response = make_response(xml_sitemap)
    response.headers["Content-Type"] = "application/xml; charset=UTF-8"
    return response


@bp.route("/feeds/all.xml")
# @cache.cached(timeout=3600)
def blog_all_feed():
    try:
        blog_data = page_details_by_type("blog.BlogIndexPage")
        blog_data = blog_data["items"][0]
        blog_posts = blog_posts_paginated(1, limit=100)
        blog_posts = blog_posts["items"]
    except ConnectionError:
        return CachedResponse(
            response=make_response(render_template("errors/api.html"), 502),
            timeout=1,
        )
    except ApiResourceNotFound:
        return CachedResponse(
            response=make_response(
                render_template("errors/page-not-found.html"), 404
            ),
            timeout=1,
        )
    except Exception:
        return CachedResponse(
            response=make_response(render_template("errors/api.html"), 502),
            timeout=1,
        )
    xml = render_template(
        "main/feed.xml",
        url=url_for("main.blog_all_feed", _external=True, _scheme="https"),
        blog_data=blog_data,
        blog_posts=blog_posts,
    )
    response = make_response(xml)
    response.headers["Content-Type"] = "application/atom+xml; charset=UTF-8"
    return response


@bp.route("/feeds/<int:blog_id>.xml")
# @cache.cached(timeout=3600)
def blog_feed(blog_id):
    try:
        blog_data = page_details(blog_id)
        blog_posts = blog_posts_paginated(1, blog_id=blog_id, limit=100)
        blog_posts = blog_posts["items"]
    except ConnectionError:
        return CachedResponse(
            response=make_response(render_template("errors/api.html"), 502),
            timeout=1,
        )
    except ApiResourceNotFound:
        return CachedResponse(
            response=make_response(
                render_template("errors/page-not-found.html"), 404
            ),
            timeout=1,
        )
    except Exception:
        return CachedResponse(
            response=make_response(render_template("errors/api.html"), 502),
            timeout=1,
        )
    xml = render_template(
        "main/feed.xml",
        url=url_for(
            "main.blog_feed", blog_id=blog_id, _external=True, _scheme="https"
        ),
        blog_data=blog_data,
        blog_posts=blog_posts,
    )
    response = make_response(xml)
    response.headers["Content-Type"] = "application/atom+xml; charset=UTF-8"
    return response


@bp.route("/logo-adornments.css")
@cache.cached(timeout=3600)
def logo_adornments_css():
    now = datetime.now()
    now_day = now.day
    now_month = now.month
    now_year = now.year
    cal = calendar.Calendar(firstweekday=calendar.MONDAY)
    november_calendar_this_year = cal.monthdatescalendar(now.year, 11)
    second_sunday_in_november_this_year = [
        day
        for week in november_calendar_this_year
        for day in week
        if day.weekday() == calendar.SUNDAY and day.month == 11
    ][1].day
    logo_adornment = ""
    if (
        now_month == 11
        and now_day >= 2
        and (now_day <= max(11, second_sunday_in_november_this_year))
    ):
        logo_adornment = "remembrance"
    elif now_month == 2:
        logo_adornment = "progress"
    elif now_month == 6:
        logo_adornment = "pride"
    elif now_month == 10:
        logo_adornment = "black-history"
    elif now_day == 15 and now_month == 3 and now_year == 2025:
        logo_adornment = "comic-relief"
    elif now_day == 22 and now_month == 4 and now_year == 2025:
        logo_adornment = "earth-day"
    css = render_template(
        "main/logo-adornments.css",
        logo_adornment=logo_adornment,
    )
    response = make_response(css)
    response.headers["Content-Type"] = "text/css; charset=UTF-8"
    return response


@bp.route("/new-homepage/")
@cache.cached(key_prefix=cache_key_prefix)
def new_homepage():
    return render_template("main/new_home.html")
