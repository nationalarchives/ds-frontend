import html
import json
import os
from urllib.parse import quote, unquote

from app.lib.cache import cache, page_cache_key_prefix
from app.lib.util import strtobool
from app.main import bp
from app.wagtail.api import global_alerts
from flask import current_app, make_response, redirect, render_template, request
from werkzeug.utils import secure_filename


@bp.route("/healthcheck/live/")
def healthcheck():
    return "ok"


@bp.route("/browse/")
@cache.cached(key_prefix=page_cache_key_prefix)
def browse():
    return render_template("main/browse.html", global_alert=global_alerts())


@bp.route("/merlin/")
@cache.cached(key_prefix=page_cache_key_prefix)
def merlin():
    return render_template("main/merlin.html", global_alert=global_alerts())


@bp.route("/cookies/set/", methods=["POST"])
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
        strtobool(html.escape(request.form["usage"].replace("\\", "")))
        if "usage" in request.form
        else bool(current_cookies_policy["usage"])
    )
    settings = (
        strtobool(html.escape(request.form["settings"].replace("\\", "")))
        if "settings" in request.form
        else bool(current_cookies_policy["settings"])
    )
    marketing = (
        strtobool(html.escape(request.form["marketing"].replace("\\", "")))
        if "marketing" in request.form
        else bool(current_cookies_policy["marketing"])
    )
    new_cookies_policy = {
        "usage": usage,
        "settings": settings,
        "marketing": marketing,
        "essential": True,
    }
    referrer = request.form.get("referrer", "/cookies/")
    response = make_response(redirect(f"{referrer}?saved=true"))
    response.set_cookie(
        "cookies_policy",
        quote(json.dumps(new_cookies_policy, separators=(",", ":"))),
        domain=current_app.config.get("COOKIE_DOMAIN"),
        secure=True,
        samesite="Lax",
    )
    response.set_cookie(
        "dontShowCookieNotice",
        "true",
        domain=current_app.config.get("COOKIE_DOMAIN"),
        secure=True,
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


@bp.route("/.well-known/<path:filename>")
def well_known(filename):
    static_file = f".well-known/{secure_filename(filename)}"
    if os.path.exists(os.path.join(current_app.static_folder, static_file)):
        return current_app.send_static_file(static_file)
    return render_template("errors/page_not_found.html"), 404
