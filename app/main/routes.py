import json
from urllib.parse import quote, unquote

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
        secure=True,
        httponly=True,
        samesite="Lax",
    )
    response.set_cookie(
        "cookie_preferences_set",
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
    return render_template("main/new_home.html")
