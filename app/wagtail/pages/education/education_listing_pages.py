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
from app.lib.pagination import pagination_object
from app.wagtail.api import education_item_paginated


def education_listing_page(page_data, api_endpoint):
    children_per_page = 12
    page = 1

    if request.args.get("page"):
        try:
            page = int(request.args.get("page", 1))
        except ValueError:
            return bad_request_error()
    if page < 1:
        return bad_request_error()

    # query = unquote(request.args.get("q", "")).strip(" ")
    query = ""

    qs = QueryStringTransformer(list(request.args.lists()))

    filters = {
        "key_stage": None,
        "location": None,
        "region": None,
        "time_period": None,
        "theme": None,
    }
    selected_filters_count = 0
    for filter_name in filters:
        if qs.parameter_exists(filter_name):
            requested_values = qs.parameter_values(filter_name)
            filter_value_key = "stage" if filter_name == "key_stage" else "slug"
            allowed_values = [
                str(value[filter_value_key])
                for value in objects.get(page_data, f"search_filters.{filter_name}", [])
            ]
            all_values_allowed = (
                all(value in allowed_values for value in requested_values)
                if requested_values
                else True
            )
            if not all_values_allowed:
                return bad_request_error()
            filters[filter_name] = requested_values
            selected_filters_count += len(requested_values)

    try:
        results_data = education_item_paginated(
            api_endpoint=api_endpoint,
            page=page,
            query=query,
            key_stages=filters["key_stage"],
            locations=filters["location"],
            regions=filters["region"],
            time_periods=filters["time_period"],
            themes=filters["theme"],
            limit=children_per_page,
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

    total_results = objects.get(results_data, "meta.total_count", 0)
    pages = math.ceil(total_results / children_per_page) if total_results > 0 else 1
    try:
        pagination = pagination_object(page, pages, request.args)
    except AssertionError:
        # The requested page is out of range, 404
        return page_not_found_error()

    return render_template(
        "education/listing-og.html"
        if "og" in request.args
        else "education/listing.html",
        q=query,
        page_data=page_data,
        children=results_data["items"],
        pagination=pagination,
        page=page,
        pages=pages,
        children_per_page=children_per_page,
        total_results=total_results,
        filtered_results=selected_filters_count > 0,
        selected_filters_count=selected_filters_count,
    )


@cacheable_duration(3600)
def education_sessions_listing_page(page_data):
    return education_listing_page(page_data, "education/sessions")


@cacheable_duration(3600)
def education_teaching_resources_listing_page(page_data):
    return education_listing_page(page_data, "education/resources")
