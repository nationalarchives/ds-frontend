from tna_utilities.component import tna_frontend_pagination


def pagination(qs, pages, page):
    pagination = None

    if pages:
        pagination_queries = qs.new().remove_parameter("page")
        if pagination_queries.get_query_string():
            base_pagination_url = pagination_queries.get_query_string() + "&page="
        else:
            base_pagination_url = "?page="
        pagination = tna_frontend_pagination(pages, page, base_pagination_url)

    return pagination
