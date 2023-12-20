from app.lib import cache, cache_key_prefix
from app.search import bp
from flask import render_template, request


@bp.route("/")
@cache.cached(key_prefix=cache_key_prefix)
def index():
    query = request.args["q"] if "q" in request.args else ""
    return render_template(
        "search/index.html",
        query=query,
    )


@bp.route("/featured/")
@cache.cached(key_prefix=cache_key_prefix)
def featured():
    query = request.args["q"] if "q" in request.args else ""
    return render_template(
        "search/featured.html",
        query=query,
    )


@bp.route("/catalogue/")
@cache.cached(key_prefix=cache_key_prefix)
def catalogue():
    query = request.args["q"] if "q" in request.args else ""
    return render_template(
        "search/catalogue.html", query=query, search_path="/search/catalogue/"
    )


@bp.route("/website/")
@cache.cached(key_prefix=cache_key_prefix)
def website():
    query = request.args["q"] if "q" in request.args else ""
    return render_template(
        "search/website.html", query=query, search_path="/search/website/"
    )
