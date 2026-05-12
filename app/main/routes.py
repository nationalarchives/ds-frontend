import html
import json
import os
from urllib.parse import quote, unquote

from flask import (
    current_app,
    make_response,
    redirect,
    render_template,
    request,
    send_from_directory,
)
from werkzeug.exceptions import NotFound

from app.lib.util import strtobool
from app.main import bp
from app.wagtail.api import global_alerts


@bp.route("/healthcheck/live/")
def healthcheck():
    return "ok"


@bp.route("/healthcheck/version/")
def healthcheck_version():
    return current_app.config["BUILD_VERSION"]


@bp.route("/merlin/")
def merlin():
    return render_template("main/merlin.html", global_alert=global_alerts())


@bp.route("/400/")
def bad_request():
    return render_template("errors/bad_request.html"), 400


@bp.route("/403/")
def forbidden():
    return render_template("errors/forbidden.html"), 403


@bp.route("/404/")
def page_not_found():
    return render_template("errors/page_not_found.html"), 404


@bp.route("/500/")
def server_error():
    return render_template("errors/server.html"), 500


@bp.route("/502/")
def api_error():
    return render_template("errors/api.html"), 502


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
    if not referrer.startswith("/"):
        referrer = "/cookies/"
    response = make_response(redirect(f"{referrer}?saved=true"))
    response.set_cookie(
        "cookies_policy",
        quote(json.dumps(new_cookies_policy, separators=(",", ":"))),
        domain=current_app.config["COOKIE_DOMAIN"],
        max_age=31536000,  # 365 days
        secure=True,
        samesite="Lax",
        httponly=False,
    )
    response.set_cookie(
        current_app.config["COOKIE_PREFERENCES_KEY"],
        "true",
        domain=current_app.config["COOKIE_DOMAIN"],
        max_age=31536000,  # 365 days
        secure=True,
        samesite="Lax",
        httponly=False,
    )
    if not usage:
        for cookie in request.cookies:
            if cookie.startswith("_ga"):
                response.delete_cookie(cookie)
    return response


@bp.route("/service-worker.min.js")
def service_worker():
    return current_app.send_static_file("service-worker.min.js")


@bp.route("/manifest.json")
def manifest():
    return current_app.send_static_file("manifest.json")


@bp.route("/robots.txt")
def robots():
    return current_app.send_static_file("robots.txt")


@bp.route("/.well-known/<path:filename>")
def well_known(filename):
    try:
        return send_from_directory(
            os.path.join(current_app.root_path, "static", ".well-known"), filename
        )
    except NotFound:
        return render_template("errors/page_not_found.html"), 404
