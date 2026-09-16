import math
from urllib.parse import unquote

from flask import render_template, request
from pydash import objects
from tna_utilities.flask import cacheable_duration
from tna_utilities.url import QueryStringTransformer

from app.error_pages.routes import bad_request_error, page_not_found_error
from app.lib.pagination import pagination
from app.search import bp
from app.wagtail.api import global_alerts, search


@bp.route("/")
@cacheable_duration(3600)
def index():
    children_per_page = 12
    page = 1
    if request.args.get("page"):
        try:
            page = int(request.args.get("page", 1))
        except ValueError:
            return bad_request_error()
    if page < 1:
        return bad_request_error()
    query = unquote(request.args.get("q", "")).strip(" ")

    # results = search(query, page, children_per_page) if query else []
    results = search(query, page, children_per_page)
    total_results = objects.get(results, "meta.total_count", 0)
    pages = math.ceil(total_results / children_per_page)

    if page > pages > 0:
        return page_not_found_error()

    qs = QueryStringTransformer(list(request.args.lists()), tolerant=True)

    return render_template(
        "search/index.html",
        q=query,
        global_alert=global_alerts(),
        results=results,
        page=page,
        pages=pages,
        children_per_page=children_per_page,
        total_results=total_results,
        pagination=pagination(qs, pages, page),
    )
