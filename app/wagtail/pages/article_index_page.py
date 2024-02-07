import math

from app.lib import pagination_list
from app.wagtail.api import breadcrumbs, page_children_paginated, page_details
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
    try:
        children = [
            page_details(child["id"]) for child in children_data["items"]
        ]
        featured_article = page_details(page_data["featured_article"]["id"])
        featured_pages = [
            page_details(featured_page_id)
            for featured_page_id in page_data["featured_pages"][0]["value"][
                "items"
            ]
        ]
    except ConnectionError:
        return render_template("errors/api.html"), 502
    return render_template(
        "explore/stories.html",
        breadcrumbs=breadcrumbs(page_data["id"]),
        page_data=page_data,
        children=children,
        featured_article=featured_article,
        featured_pages=featured_pages,
        pagination_list=pagination_list(page, pages),
        page=page,
        pages=pages,
    )
