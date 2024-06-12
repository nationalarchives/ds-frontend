import json
from urllib.parse import quote, unquote

from app.legal import bp
from app.lib import cache, cache_key_prefix
from app.lib.util import strtobool
from flask import make_response, render_template, request, current_app


@bp.route("/")
@cache.cached(key_prefix=cache_key_prefix)
def index():
    return render_template("legal/index.html")


@bp.route("/cookies/", methods=["GET", "POST"])
def cookies():
    if request.method == "POST":
        current_cookies_policy = {
            "usage": False,
            "settings": False,
            "essential": True,
        }
        if "cookies_policy" in request.cookies:
            cookies_policy = request.cookies["cookies_policy"]
            current_cookies_policy = json.loads(unquote(cookies_policy))
        new_cookies_policy = {
            "usage": (
                strtobool(request.form["usage"])
                if "usage" in request.form
                else current_cookies_policy["usage"]
            ),
            "settings": (
                strtobool(request.form["settings"])
                if "settings" in request.form
                else current_cookies_policy["settings"]
            ),
            "essential": True,
        }
        response = make_response(render_template("legal/cookies.html"))
        response.set_cookie(
            "cookies_policy",
            quote(json.dumps(new_cookies_policy, separators=(",", ":"))),
            domain=current_app.config["COOKIE_DOMAIN"]
        )
        return response
    return render_template("legal/cookies.html")


@bp.route("/cookie-details/")
@cache.cached(key_prefix=cache_key_prefix)
def cookie_details():
    return render_template("legal/cookie-details.html")
