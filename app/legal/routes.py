from app.legal import bp
from app.lib import cache, cache_key_prefix
from flask import render_template


@bp.route("/")
@cache.cached(key_prefix=cache_key_prefix)
def index():
    return render_template("legal/index.html")


@bp.route("/cookies/")
@cache.cached(key_prefix=cache_key_prefix)
def cookies():
    return render_template("legal/cookies.html")


@bp.route("/cookie-details/")
@cache.cached(key_prefix=cache_key_prefix)
def cookie_details():
    return render_template("legal/cookie-details.html")
