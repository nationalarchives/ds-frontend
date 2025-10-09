import math
from urllib.parse import unquote

from app.lib.pagination import pagination_object
from app.search import bp
from app.wagtail.api import global_alerts, search
from flask import render_template, request
from pydash import objects


@bp.route("/")
def index():
    children_per_page = 12
    page = 1
    if request.args.get("page"):
        try:
            page = int(request.args.get("page", 1))
        except ValueError:
            return render_template("errors/bad_request.html"), 400
    if page < 1:
        return render_template("errors/bad_request.html"), 400
    query = unquote(request.args.get("q", "")).strip(" ")
    existing_qs_as_dict = request.args.to_dict()
    # results = search(query, page, children_per_page) if query else []
    results = search(query, page, children_per_page)
    total_results = objects.get(results, "meta.total_count", 0)
    pages = math.ceil(total_results / children_per_page)
    try:
        pagination = pagination_object(page, pages, request.args)
    except AssertionError:
        # The requested page is out of range, 404
        return render_template("errors/page_not_found.html"), 404
    return render_template(
        "search/index.html",
        q=query,
        existing_qs=existing_qs_as_dict,
        global_alert=global_alerts(),
        results=results,
        page=page,
        pages=pages,
        children_per_page=children_per_page,
        total_results=total_results,
        pagination=pagination,
    )
