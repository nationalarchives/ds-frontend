import math

from app.lib.datetime import group_items_by_year_and_month
from app.lib.pagination import pagination_object
from app.wagtail.api import foi_requests
from flask import current_app, render_template, request


def foi_index_page(page_data):
    children_per_page = 50
    page = 1
    if request.args.get("page"):
        try:
            page = int(request.args.get("page", 1))
        except ValueError:
            return render_template("errors/bad_request.html"), 400
    if page < 1:
        return render_template("errors/bad_request.html"), 400
    try:
        requests_raw = foi_requests(
            page,
            children_per_page,
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

    requests = group_items_by_year_and_month(requests_raw, "date")

    pages = math.ceil(requests_raw["meta"]["total_count"] / children_per_page)
    try:
        pagination = pagination_object(page, pages, request.args)
    except AssertionError:
        # The requested page is out of range, 404
        return render_template("errors/page_not_found.html"), 404

    return render_template(
        "foi/index.html",
        page_data=page_data,
        requests=requests,
        pagination=pagination,
        page=page,
        pages=pages,
    )
