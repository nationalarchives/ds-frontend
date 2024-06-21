from app.about import bp
from app.lib import cache, cache_key_prefix
from flask import render_template


@bp.route("/")
@cache.cached(key_prefix=cache_key_prefix)
def index():
    return render_template("about/index.html")


@bp.route("/freedom-of-information/")
@cache.cached(key_prefix=cache_key_prefix)
def freedom_of_information():
    return render_template("about/freedom_of_information.html")
