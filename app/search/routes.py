from app.lib import cache
from app.search import bp
from flask import render_template, request


def make_cache_key_prefix():
    """Make a key that includes GET parameters."""
    return request.full_path


@bp.route("/")
@cache.cached()
def index():
    return render_template(
        "search/index.html",
    )
