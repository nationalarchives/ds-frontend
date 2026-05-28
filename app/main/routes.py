import html
import json
import os
from urllib.parse import quote, unquote, urlparse

from flask import (
    current_app,
    make_response,
    redirect,
    render_template,
    request,
    send_from_directory,
)
from tna_utilities import strtobool
from werkzeug.exceptions import NotFound

from app.error_pages.routes import page_not_found_error
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


@bp.route("/cookies/set/", methods=["POST"])
def set_cookies():
    current_cookies_policy = {
        "usage": False,
        "settings": False,
        "marketing": False,
        "essential": True,
    }
    if current_app.config["COOKIE_PREFERENCES_KEY"] in request.cookies:
        current_cookies_policy = json.loads(
            unquote(request.cookies[current_app.config["COOKIE_PREFERENCES_KEY"]])
        )
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
    referrer = request.form.get("referrer", "/cookies/?saved=true")
    referrer = referrer.replace("\\", "")
    parsed_referrer = urlparse(referrer)
    if (
        not referrer.startswith("/")
        or parsed_referrer.netloc
        or parsed_referrer.scheme
    ):
        referrer = "/cookies/?saved=true"
    response = make_response(redirect(referrer))
    response.set_cookie(
        current_app.config["COOKIE_PREFERENCES_KEY"],
        quote(json.dumps(new_cookies_policy, separators=(",", ":"))),
        domain=current_app.config["COOKIE_DOMAIN"],
        max_age=31536000,  # 365 days
        secure=True,
        samesite="Lax",
        httponly=False,
    )
    response.set_cookie(
        current_app.config["COOKIE_PREFERENCES_SET_KEY"],
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
    # TODO: Replace with @vary_by_cookies decorator when released
    response.headers["Vary"] = "Cookie"
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
        return page_not_found_error()
