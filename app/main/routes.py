import json
from urllib.parse import quote, unquote

from app.lib.cache import cache, page_cache_key_prefix
from app.lib.util import strtobool
from app.main import bp
from app.wagtail.api import global_alerts
from app.wagtail.pages import (
    display_page,
    event_page,
    events_page,
    exhibitions_page,
    whats_on_search_page,
    whats_on_series_page,
)
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
        "dontShowCookieNotice",
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


@bp.route("/test/homepage/")
@cache.cached(key_prefix=page_cache_key_prefix)
def new_homepage():
    return render_template("main/new_home.html")


@bp.route("/whats-on/events/")
def test_events_page():
    return events_page(
        page_data={
            "id": 0,
            "title": "Events",
        }
    )


@bp.route("/whats-on/events/1/")
def test_event_page():
    return event_page(
        page_data={
            "id": 0,
            "title": "Event #1",
        }
    )


@bp.route("/whats-on/exhibitions/")
def test_exhibitions_page():
    return exhibitions_page(
        page_data={
            "id": 0,
            "title": "Exhibitions",
        }
    )


@bp.route("/whats-on/exhibitions/display/")
def test_display_page():
    return display_page(
        page_data={
            "id": 0,
            "title": "Displays",
        }
    )


@bp.route("/whats-on/search/")
def test_search_page():
    return whats_on_search_page(
        page_data={
            "id": 0,
            "title": "Search",
        }
    )


@bp.route("/whats-on/series/")
def test_series_page():
    return whats_on_series_page(
        page_data={
            "id": 0,
            "title": "Series",
        }
    )
