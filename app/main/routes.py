import json
from urllib.parse import quote, unquote, urlparse

from app.eventbrite.api import event_details, tna_events
from app.lib import cache, cache_key_prefix, pagination_object
from app.lib.template_filters import slugify
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


@bp.route("/test/new-homepage/")
@cache.cached(key_prefix=cache_key_prefix)
def new_homepage():
    return render_template("main/test-new-home.html")


@bp.route("/test/whats-on/")
@cache.cached(key_prefix=cache_key_prefix)
def whats_on():
    event_ids = [
        # Main events for testing
        948911348387,
        998391775677,
        998387051547,
        953481136747,
        # Additional events
        1000012633707,
        998381103757,
        953390846687,
        998406218877,
        998417723287,
        998434022037,
        998435867557,
        998444222547,
        998447141277,
        998456719927,
        998461674747,
        998463821167,
        998466248427,
    ]
    children_per_page = 5
    page = (
        int(request.args.get("page"))
        if "page" in request.args and request.args["page"].isnumeric()
        else 1
    )
    all_events = tna_events(
        page,
        children_per_page,
        {"event_ids": ",".join([str(id) for id in event_ids])},
    )
    pages = all_events["pagination"]["page_count"]
    if page > pages:
        return render_template("errors/page-not-found.html"), 404
    pagination = pagination_object(page, pages, request.args)
    events = all_events["events"]
    return render_template(
        "main/test-whats-on.html", events=events, pagination=pagination
    )


@bp.route("/test/whats-on/<string:slug>-<int:event_id>/")
@cache.cached(key_prefix=cache_key_prefix)
def event(slug, event_id):
    event = event_details(event_id)
    if slug != slugify(event["name"]["text"]):
        return render_template("errors/page-not-found.html"), 404
        # return redirect(
        #     url_for("main.event", slug=slugify(event["name"]["text"]), event_id=event_id)
        # )
    return render_template("main/test-whats-on-event.html", event=event)
