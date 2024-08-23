import json
from urllib.parse import quote, unquote

from app.legal import bp
from app.lib import cache, cache_key_prefix
from app.lib.util import strtobool
from app.wagtail.api import global_alerts
from flask import (
    current_app,
    make_response,
    redirect,
    render_template,
    request,
    url_for,
)


@bp.route("/")
# @cache.cached(key_prefix=cache_key_prefix)
def index():
    return render_template("legal/index.html")


@bp.route("/cookies/", methods=["GET", "POST"])
def cookies():
    if request.method == "POST":
        current_cookies_policy = {
            "usage": False,
            "settings": False,
            "marketing": False,
            "essential": True,
        }
        if "cookies_policy" in request.cookies:
            cookies_policy = request.cookies["cookies_policy"]
            current_cookies_policy = json.loads(unquote(cookies_policy))
        usage = (
            strtobool(request.form["usage"])
            if "usage" in request.form
            else current_cookies_policy["usage"]
        )
        settings = (
            strtobool(request.form["settings"])
            if "settings" in request.form
            else current_cookies_policy["settings"]
        )
        marketing = (
            strtobool(request.form["marketing"])
            if "marketing" in request.form
            else current_cookies_policy["marketing"]
        )
        new_cookies_policy = {
            "usage": usage,
            "settings": settings,
            "marketing": marketing,
            "essential": True,
        }
        response = make_response(
            redirect(
                url_for(
                    "legal.cookies",
                    saved="true",
                    referrer=(
                        request.form["referrer"]
                        if "referrer" in request.form
                        else ""
                    ),
                )
            )
        )
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
    return render_template(
        "legal/cookies.html",
        global_alerts=global_alerts(),
        page_data={
            "title": "Cookies",
            "intro": f"""<p>Cookies are files saved on your phone, tablet or computer when you visit a website.</p>
<p>We use cookies to collect and store information about how you use National Archives websites which means any page with nationalarchives.gov.uk in the URL.</p>
<p>This page has a brief explanation of each type of cookie we use. If you want more details, <a href="{url_for('legal.cookie_details')}">our detailed cookie information</a>.</p>""",
        },
    )


@bp.route("/cookie-details/")
# @cache.cached(key_prefix=cache_key_prefix)
def cookie_details():
    return render_template(
        "legal/cookie-details.html", global_alerts=global_alerts()
    )
