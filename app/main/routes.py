import json
from urllib.parse import quote, unquote

from app.eventbrite.api import event_details, tna_events
from app.lib.pagination import pagination_object
from app.lib.template_filters import slugify
from app.lib.cache import cache, page_cache_key_prefix
from app.lib.util import strtobool
from app.main import bp
from app.wagtail.api import global_alerts
from flask import current_app, make_response, redirect, render_template, request


@bp.route("/healthcheck/live/")
def healthcheck():
    return "ok"


@bp.route("/browse/")
@cache.cached(key_prefix=page_cache_key_prefix)
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


@bp.route("/new-homepage/")
@cache.cached(key_prefix=page_cache_key_prefix)
def new_homepage():
    return render_template("main/test-new-home.html")


@bp.route("/test/whats-on/")
@cache.cached(key_prefix=page_cache_key_prefix)
def whats_on():
    event_ids = [
        948911348387,
        998391775677,
        998387051547,
        953481136747,
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
    children_per_page = 12
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
    print(all_events["pagination"])
    return render_template(
        "main/test-whats-on.html",
        events=events,
        page=page,
        events_per_page=children_per_page,
        total_events=all_events["pagination"]["object_count"],
        pagination=pagination,
    )


@bp.route("/test/whats-on/<string:slug>-<int:event_id>/")
@cache.cached(key_prefix=page_cache_key_prefix)
def event(slug, event_id):
    event = event_details(event_id)
    if slug != slugify(event["name"]["text"]):
        return render_template("errors/page-not-found.html"), 404
        # return redirect(
        #     url_for("main.event", slug=slugify(event["name"]["text"]), event_id=event_id)
        # )
    return render_template("main/test-whats-on-event.html", event=event)
