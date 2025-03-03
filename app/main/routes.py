import json
from urllib.parse import quote, unquote

from app.eventbrite.api import event_details, tna_events, tna_events_by_date
from app.lib.cache import cache, page_cache_key_prefix
from app.lib.pagination import pagination_object
from app.lib.template_filters import slugify
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
        current_cookies_policy = json.loads(unquote(request.cookies["cookies_policy"]))
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
        secure=True,
        httponly=True,
        samesite="Lax",
    )
    response.set_cookie(
        # "cookie_preferences_set",
        "dontShowCookieNotice",  # TODO: Change once more pages are on the new frontend
        "true",
        domain=current_app.config.get("COOKIE_DOMAIN"),
        secure=True,
        httponly=True,
        samesite="Lax",
    )
    if not usage:
        for cookie in request.cookies:
            if cookie.startswith("_ga"):
                response.delete_cookie(cookie)
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
    event_ids = ",".join(
        [
            str(id)
            for id in [
                1227466357919,
                1227509246199,
                1230051279489,
            ]
        ]
    )
    children_per_page = 12
    year = (
        int(request.args.get("year"))
        if request.args.get("year") and request.args.get("year").isnumeric()
        else None
    )
    month = (
        int(request.args.get("month"))
        if request.args.get("month") and request.args.get("month").isnumeric()
        else None
    )
    day = (
        int(request.args.get("day"))
        if request.args.get("day") and request.args.get("day").isnumeric()
        else None
    )
    page = (
        int(request.args.get("page"))
        if "page" in request.args and request.args["page"].isnumeric()
        else 1
    )
    all_events = (
        tna_events(
            page,
            children_per_page,
            {"event_ids": event_ids},
        )
        if not (year or month or day)
        else tna_events_by_date(
            page, children_per_page, year, month, day, {"event_ids": event_ids}
        )
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
        pages=pages,
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
