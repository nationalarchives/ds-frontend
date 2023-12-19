from app.lib import cache
from app.search import bp
from flask import render_template, request


def make_cache_key_prefix():
    """Make a key that includes GET parameters."""
    return request.full_path


@bp.route("/")
@cache.cached()
def index():
    query = request.args["q"] if "q" in request.args else ""
    return render_template(
        "search/index.html",
        query=query,
    )


@bp.route("/featured/")
@cache.cached()
def featured():
    query = request.args["q"] if "q" in request.args else ""
    return render_template(
        "search/featured.html",
        query=query,
    )


@bp.route("/catalogue/")
@cache.cached()
def catalogue():
    query = request.args["q"] if "q" in request.args else ""
    return render_template(
        "search/catalogue.html", query=query, search_path="/search/catalogue/"
    )


@bp.route("/website/")
@cache.cached()
def website():
    query = request.args["q"] if "q" in request.args else ""
    return render_template(
        "search/website.html", query=query, search_path="/search/website/"
    )
