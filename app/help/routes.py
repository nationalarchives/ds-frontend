from app.help import bp
from app.lib import cache, cache_key_prefix
from flask import render_template


@bp.route("/")
@cache.cached(key_prefix=cache_key_prefix)
def index():
    return render_template("help/index.html")


@bp.route("/accessibility/")
@cache.cached(key_prefix=cache_key_prefix)
def accessibility():
    return render_template("help/accessibility.html")


@bp.route("/a-to-z/")
@cache.cached(key_prefix=cache_key_prefix)
def a_to_z():
    return render_template("help/a-to-z.html")


@bp.route("/discovery-for-developers/")
@cache.cached(key_prefix=cache_key_prefix)
def discovery_for_developers():
    return render_template("help/discovery-for-developers.html")
