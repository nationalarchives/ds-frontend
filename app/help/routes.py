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
