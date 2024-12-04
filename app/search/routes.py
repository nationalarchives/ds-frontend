import math
from urllib.parse import unquote

from app.lib.pagination import pagination_object
from app.search import bp
from app.wagtail.api import global_alerts, search
from flask import render_template, request, url_for
from pydash import objects

"""
Align paths to routes in https://github.com/nationalarchives/ds-search
"""


message = (
    "Replaced with the contents of ds-search in dev, staging and production"
)


@bp.route("/")
def index():
    return message


@bp.route("/catalogue/")
def catalogue():
    return message


@bp.route("/catalogue/id/<id>")
def catalogue_item(id):
    return message


@bp.route("/site/")
def site():
    breadcrumbs = [
        {"text": "Home", "href": "/"},
        {"text": "Search", "href": url_for("search.index")},
    ]
    children_per_page = 12
    page = (
        int(request.args.get("page"))
        if request.args.get("page") and request.args.get("page").isnumeric()
        else 1
    )
    query = unquote(request.args.get("q", "")).strip(" ")
    existing_qs_as_dict = request.args.to_dict()
    # results = search(query, page, children_per_page) if query else []
    results = search(query, page, children_per_page)
    total_results = objects.get(results, "meta.total_count", 0)
    pages = math.ceil(total_results / children_per_page)
    # if query and page > pages:
    #     return render_template("errors/page-not-found.html"), 404
    return render_template(
        "site_search/index.html",
        q=query,
        existing_qs=existing_qs_as_dict,
        global_alert=global_alerts(),
        breadcrumbs=breadcrumbs,
        results=results,
        page=page,
        pages=pages,
        children_per_page=children_per_page,
        total_results=total_results,
        pagination=pagination_object(page, pages, request.args),
    )
