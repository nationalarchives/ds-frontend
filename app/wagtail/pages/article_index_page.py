import math

from app.lib import pagination_object
from app.wagtail.api import breadcrumbs, page_children_paginated
from flask import render_template, request


def article_index_page(page_data):
    children_per_page = 12
    page = int(request.args.get("page")) if "page" in request.args else 1
    try:
        children_data = page_children_paginated(
            page_data["id"], page, children_per_page
        )
    except ConnectionError:
        return render_template("errors/api.html"), 502
    pages = math.ceil(children_data["meta"]["total_count"] / children_per_page)
    if page > pages:
        return render_template("errors/page-not-found.html"), 404
    return render_template(
        "explore/stories.html",
        breadcrumbs=breadcrumbs(page_data["id"]),
        page_data=page_data,
        children=children_data["items"],
        pagination=pagination_object(page, pages, request.args),
        page=page,
        pages=pages,
    )
