import math

from flask import current_app, render_template, request
from pydash import objects
from tna_utilities.flask import cacheable_duration

from app.error_pages.routes import (
    bad_gateway_error,
    bad_request_error,
    page_not_found_error,
    server_error,
)
from app.lib.pagination import pagination_object
from app.wagtail.api import authored_pages_paginated


@cacheable_duration(3600)
def person_page(page_data):
    articles_preview_list = 4
    articles_per_page = 12
    page = 0
    if request.args.get("page"):
        try:
            page = int(request.args.get("page", 1))
        except ValueError:
            return bad_request_error()
    if page < 0:
        return bad_request_error()
    try:
        articles = authored_pages_paginated(
            author_id=page_data["id"],
            page=page or 1,
            limit=articles_per_page if page else articles_preview_list,
            params={
                "order": "-id",
            },
        )
    except ConnectionError:
        current_app.logger.exception(
            f"API error getting author articles for page {page_data['id']}"
        )
        return bad_gateway_error()
    except Exception:
        current_app.logger.exception(
            f"Exception getting author articles for page {page_data['id']}"
        )
        return server_error()
    total_article_count = objects.get(articles, "meta.total_count", 0)
    articles = objects.get(articles, "items", [])
    pages = math.ceil(total_article_count / articles_per_page)
    if page > pages:
        return page_not_found_error()
    return render_template(
        "people/person.html",
        page_data=page_data,
        pagination=pagination_object(page, pages, request.args),
        page=page,
        pages=pages,
        articles=articles,
        more_articles=total_article_count > articles_preview_list,
    )
