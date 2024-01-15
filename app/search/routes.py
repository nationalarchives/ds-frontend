import urllib.parse

from app.lib import cache, cache_key_prefix, pagination_object
from app.lib.query import parse_args, remove_arg
from app.lib.template_filters import slugify
from app.search import bp
from flask import render_template, request, url_for

from .api import ArticleFiltersAPI, ArticlesAPI, RecordFiltersAPI, RecordsAPI


@bp.route("/")
@cache.cached(key_prefix=cache_key_prefix)
def index():
    query = request.args["q"] if "q" in request.args else ""
    return render_template(
        "search/index.html",
        query=query,
        search_path=url_for("search.featured"),
    )


@bp.route("/featured/")
@cache.cached(key_prefix=cache_key_prefix)
def featured():
    query = request.args["q"] if "q" in request.args else ""
    return render_template(
        "search/featured.html",
        query=query,
        search_path=url_for("search.catalogue"),
    )


@bp.route("/catalogue/")
@cache.cached(key_prefix=cache_key_prefix)
def catalogue():
    query = request.args["q"] if "q" in request.args else ""
    page = int(request.args["page"]) if "page" in request.args else 1
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
    filters = get_filters(RecordFiltersAPI, args)
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
    )


@bp.route("/catalogue-new/")
@cache.cached(key_prefix=cache_key_prefix)
def catalogue_new():
    query = request.args["q"] if "q" in request.args else ""
    return render_template(
        "search/catalogue-new.html",
        query=query,
        search_path=url_for("search.catalogue"),
    )


@bp.route("/website/")
@cache.cached(key_prefix=cache_key_prefix)
def website():
    query = request.args["q"] if "q" in request.args else ""
    page = int(request.args["page"]) if "page" in request.args else 1
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
    filters = get_filters(ArticleFiltersAPI, args)
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
    )


def get_filters(api, args):
    filters_api = api()
    filters_api.params = (
        {}
    )  # TODO: Why do I need to do this? Things are persisting...
    return [
        {
            "title": filter["title"],
            "type": filter["type"],
            "slug": slugify(filter["title"]),
            "value": args[slugify(filter["title"])]
            if filter["type"] == "text" and slugify(filter["title"]) in args
            else "",
            "options": [
                {
                    "text": option["name"],
                    "value": option["value"],
                    "checked": (
                        str(option["value"]) in args[slugify(filter["title"])]
                    )
                    if slugify(filter["title"]) in args
                    else False,
                    "remove_url": remove_arg(
                        request.args, slugify(filter["title"]), option["value"]
                    ),
                }
                for option in filter["options"]
            ]
            if filter["type"] == "multiple"
            else [],
        }
        for filter in filters_api.get_results()
    ]


def get_selected_filters(filters):
    selected_filters = []
    for filter in filters:
        if filter["type"] == "multiple":
            for option in filter["options"]:
                if option["checked"]:
                    selected_filters.append(
                        {
                            "group": filter["title"],
                            "filter": option["text"],
                            "remove_url": option["remove_url"],
                        }
                    )
        if filter["type"] == "text" and filter["value"]:
            selected_filters.append(
                {
                    "group": filter["title"],
                    "filter": filter["value"],
                    "remove_url": remove_arg(
                        request.args, slugify(filter["title"])
                    ),
                }
            )
    return selected_filters
