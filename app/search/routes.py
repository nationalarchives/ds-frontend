from app.lib import cache, cache_key_prefix
from app.search import bp
from flask import render_template, request

from .api import ArticleFiltersAPI, ArticlesAPI, RecordsAPI


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
    records_api = RecordsAPI()
    records_api.query(query)
    results = records_api.get_results()
    return render_template(
        "search/catalogue.html",
        query=query,
        search_path="/search/catalogue/",
        results=results,
    )


@bp.route("/catalogue-new/")
@cache.cached(key_prefix=cache_key_prefix)
def catalogue_new():
    query = request.args["q"] if "q" in request.args else ""
    return render_template(
        "search/catalogue-new.html",
        query=query,
        search_path="/search/catalogue/",
    )


@bp.route("/website/")
@cache.cached(key_prefix=cache_key_prefix)
def website():
    query = request.args["q"] if "q" in request.args else ""

    article_filters_api = ArticleFiltersAPI()
    article_filters_api.params = (
        {}
    )  # TODO: Why do I need to do this? Things are persisting...
    filters = [
        {
            "title": filter["title"],
            "options": [
                {"text": option["name"], "value": option["value"]}
                for option in filter["options"]
            ],
        }
        for filter in article_filters_api.get_results()
    ]

    articles_api = ArticlesAPI()
    articles_api.params = (
        {}
    )  # TODO: Why do I need to do this? Things are persisting...
    if query:
        articles_api.query(query)
    if "type[]" in request.args:
        types = request.args.to_dict(flat=False)["type[]"]
        articles_api.add_parameter("type", ",".join(types))
    results = articles_api.get_results()

    return render_template(
        "search/website.html",
        query=query,
        search_path="/search/website/",
        results=results,
        filters=filters,
    )
