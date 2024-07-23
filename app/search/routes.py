from app.lib import cache, cache_key_prefix, pagination_object
from app.lib.query import parse_args
from app.search import bp
from app.wagtail.api import global_alert
from flask import render_template, request, url_for

from .api import ArticlesAPI, RecordsAPI
from .lib import get_filters, get_selected_filters


@bp.route("/")
@cache.cached(key_prefix=cache_key_prefix)
def index():
    query = request.args["q"] if "q" in request.args else ""
    return render_template(
        "search/index.html",
        query=query,
        search_path=url_for("search.catalogue"),
        global_alert=global_alert(),
    )


@bp.route("/featured/")
@cache.cached(key_prefix=cache_key_prefix)
def featured():
    query = request.args["q"] if "q" in request.args else ""
    return render_template(
        "search/featured.html",
        query=query,
        search_path=url_for("search.catalogue"),
        global_alert=global_alert(),
    )


@bp.route("/catalogue/")
@cache.cached(key_prefix=cache_key_prefix)
def catalogue():
    query = request.args["q"] if "q" in request.args else ""
    page = (
        int(request.args["page"])
        if "page" in request.args and request.args["page"].isnumeric()
        else 1
    )
    group = request.args["group"] if "group" in request.args else "tna"
    args = parse_args(request.args)
    records_api = RecordsAPI()
    records_api.query(query)
    records_api.add_parameter("groups", group)
    records_api.add_parameter("highlight", True)
    try:
        results = records_api.get_results(page)
    except ConnectionError:
        return render_template("errors/api.html"), 502
    except Exception:
        return render_template("errors/page-not-found.html"), 404
    filters = get_filters(results["filters"], args)
    selected_filters = get_selected_filters(filters)
    return render_template(
        "search/catalogue.html",
        query=query,
        group=group,
        search_path=url_for("search.catalogue"),
        results=results,
        filters=filters,
        selected_filters=selected_filters,
        page=page,
        pages=results["pages"],
        pagination=pagination_object(page, results["pages"], request.args),
        global_alert=global_alert(),
    )


@bp.route("/website/")
@cache.cached(key_prefix=cache_key_prefix)
def website():
    query = request.args["q"] if "q" in request.args else ""
    page = (
        int(request.args["page"])
        if "page" in request.args and request.args["page"].isnumeric()
        else 1
    )
    args = parse_args(request.args)
    articles_api = ArticlesAPI()
    articles_api.params = (
        {}
    )  # TODO: Why do I need to do this? Things are persisting...
    if query:
        articles_api.query(query)
    if "type[]" in request.args:
        types = request.args.to_dict(flat=False)["type[]"]
        articles_api.add_parameter("type", ",".join(types))
    if "order" in request.args:
        articles_api.add_parameter("order", request.args["order"])
    try:
        results = articles_api.get_results(page)
    except ConnectionError:
        return render_template("errors/api.html"), 502
    except Exception:
        return render_template("errors/page-not-found.html"), 404
    filters = [
        filter | {"open": True}
        for filter in get_filters(results["filters"], args)
    ]
    selected_filters = get_selected_filters(filters)
    return render_template(
        "search/website.html",
        query=query,
        search_path=url_for("search.website"),
        results=results,
        filters=filters,
        selected_filters=selected_filters,
        page=page,
        pages=results["pages"],
        pagination=pagination_object(page, results["pages"], request.args),
        global_alert=global_alert(),
    )
