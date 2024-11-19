import math

from app.lib.pagination import pagination_object
from app.site_search import bp
from app.wagtail.api import global_alerts, search
from flask import render_template, request, url_for
from pydash import objects


@bp.route("/")
def index():
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
    query = request.args.get("q", "")
    # results = search(query, page, children_per_page) if query else []
    results = search(query, page, children_per_page)
    total_results = objects.get(results, "meta.total_count", 0)
    pages = math.ceil(total_results / children_per_page)
    # if query and page > pages:
    #     return render_template("errors/page-not-found.html"), 404
    return render_template(
        "site_search/index.html",
        q=query,
        global_alert=global_alerts(),
        breadcrumbs=breadcrumbs,
        results=results,
        page=page,
        pages=pages,
        children_per_page=children_per_page,
        total_results=total_results,
        pagination=pagination_object(page, pages, request.args),
    )
