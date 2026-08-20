from tna_utilities.component import tna_frontend_pagination


def pagination(
    qs, pages, page, previous_page_properties=None, next_page_properties=None
):
    pagination = None

    if previous_page_properties is None:
        previous_page_properties = {
            "title": "Previous page",
        }

    if next_page_properties is None:
        next_page_properties = {
            "title": "Next page",
        }

    if pages:
        pagination_queries = qs.new().remove_parameter("page")
        if pagination_queries.get_query_string():
            base_pagination_url = pagination_queries.get_query_string() + "&"
        else:
            base_pagination_url = "?"
        pagination = tna_frontend_pagination(
            pages,
            page,
            base_pagination_url + "page=",
            previous_page_properties=previous_page_properties,
            next_page_properties=next_page_properties,
        )

    return pagination
