import math

from app.lib import pagination_object
from app.wagtail.api import breadcrumbs, page_children_paginated
from flask import current_app, render_template, request


def blog_index_page(page_data, year=None, month=None, day=None):
    children_per_page = 24
    page = (
        int(request.args.get("page"))
        if "page" in request.args and request.args["page"].isnumeric()
        else 1
    )
    try:
        # TODO: Filter children_data by year, month and day
        children_data = page_children_paginated(
            page_data["id"], page, children_per_page
        )
    except ConnectionError:
        current_app.logger.error(
            f"API error getting children for page {page_data['id']}"
        )
        return render_template("errors/api.html"), 502
    except Exception:
        current_app.logger.error(
            f"Exception getting children for page {page_data['id']}"
        )
        return render_template("errors/server.html"), 500
    pages = math.ceil(children_data["meta"]["total_count"] / children_per_page)
    if page > pages:
        return render_template("errors/page-not-found.html"), 404
    return render_template(
        "blog/index.html",
        breadcrumbs=breadcrumbs(page_data["id"]),
        page_data=page_data,
        children=children_data["items"],
        total_children=children_data["meta"]["total_count"],
        pagination=pagination_object(page, pages, request.args),
        page=page,
        pages=pages,
        date_filter={"year": year, "month": month, "day": day},
    )
