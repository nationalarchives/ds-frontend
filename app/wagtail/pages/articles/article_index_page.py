import math

from flask import current_app, render_template, request
from pydash import objects
from tna_utilities.flask import cacheable_duration
from tna_utilities.url import QueryStringTransformer

from app.error_pages.routes import (
    bad_gateway_error,
    bad_request_error,
    page_not_found_error,
    server_error,
)
from app.lib.pagination import pagination
from app.wagtail.api import page_children_paginated


@cacheable_duration(3600)
def article_index_page(page_data):
    children_per_page = 12
    page = 1
    if request.args.get("page"):
        try:
            page = int(request.args.get("page", 1))
        except ValueError:
            return bad_request_error()
    if page < 1:
        return bad_request_error()
    try:
        children_data = page_children_paginated(
            page_data["id"],
            page,
            children_per_page,
            params={"order": "-first_published_at"},
        )
    except ConnectionError:
        current_app.logger.exception(
            f"API error getting children for page {page_data['id']}"
        )
        return bad_gateway_error()
    except Exception:
        current_app.logger.exception(
            f"Exception getting children for page {page_data['id']}"
        )
        return server_error()
    total_results = objects.get(children_data, "meta.total_count", 0)
    pages = math.ceil(total_results / children_per_page)

    if page > pages > 0:
        return page_not_found_error()

    qs = QueryStringTransformer(list(request.args.lists()), tolerant=True)

    return render_template(
        "explore_the_collection/stories.html",
        page_data=page_data,
        children=children_data["items"],
        pagination=pagination(qs, pages, page),
        page=page,
        pages=pages,
    )
