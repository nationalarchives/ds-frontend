import math
from urllib.parse import unquote

from flask import current_app, render_template, request
from pydash import objects
from tna_utilities.flask import cacheable_duration

from app.error_pages.routes import (
    api_error,
    bad_request_error,
    page_not_found_error,
    server_error,
)
from app.lib.pagination import pagination_object
from app.wagtail.api import page_children_paginated, search


@cacheable_duration(3600)
def education_sessions_listing_page(page_data):
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

    if query:
        children_data = search(
            query,
            page=page,
            limit=children_per_page,
            params={"child_of": page_data["id"]},
        )
    else:
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
            return api_error()
        except Exception:
            current_app.logger.exception(
                f"Exception getting children for page {page_data['id']}"
            )
            return server_error()

    total_results = objects.get(children_data, "meta.total_count", 0)
    pages = math.ceil(total_results / children_per_page) if total_results > 0 else 1
    try:
        pagination = pagination_object(page, pages, request.args)
    except AssertionError:
        # The requested page is out of range, 404
        return page_not_found_error()

    return render_template(
        "education/listing.html",
        q=query,
        page_data=page_data,
        children=children_data["items"],
        pagination=pagination,
        page=page,
        pages=pages,
        children_per_page=children_per_page,
        total_results=children_data["meta"]["total_count"],
    )
