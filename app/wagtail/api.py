import requests
from app.lib.api import ApiResourceNotFound
from flask import current_app


def wagtail_request_handler(uri, params={}):
    api_url = current_app.config["WAGTAIL_API_URL"]
    if not api_url:
        current_app.logger.critical("WAGTAIL_API_URL not set")
        raise Exception("WAGTAIL_API_URL not set")
    params["format"] = "json"
    query_string = (
        "?"
        + "&".join(
            ["=".join((key, str(value))) for key, value in params.items()]
        )
        if len(params)
        else ""
    )
    url = f"{api_url}/{uri}{query_string}"
    current_app.logger.debug(f"API endpoint requested: {url}")
    r = requests.get(url)
    if r.status_code == 404:
        current_app.logger.warning(f"Resource not found: {url}")
        raise ApiResourceNotFound("Resource not found")
    if r.status_code == requests.codes.ok:
        try:
            return r.json()
        except requests.exceptions.JSONDecodeError:
            current_app.logger.error("API provided non-JSON response")
            raise ConnectionError("API provided non-JSON response")
    current_app.logger.error(
        f"API responded with {r.status_code} status for {url}"
    )
    raise ConnectionError("Request to API failed")


def breadcrumbs(page_id):
    try:
        ancestors = page_ancestors(page_id)
    except Exception:
        current_app.logger.warning(f"Page {page_id} failed to get ancestors")
        return []
    return (
        [
            {
                "text": (
                    "Home" if ancestor["url"] == "/" else ancestor["title"]
                ),
                "href": (
                    "https://www.nationalarchives.gov.uk/"
                    if ancestor["url"] == "/"
                    else ancestor["url"]
                ),
            }
            for ancestor in ancestors["items"]
        ]
        if ancestors
        else []
    )


def all_pages(batch=1, params={}):
    children_per_page = 20
    offset = (batch - 1) * children_per_page
    params = params | {"offset": offset, "limit": children_per_page}
    uri = "pages/"
    return wagtail_request_handler(uri, params)


def page_details(page_id, params={}):
    uri = f"pages/{page_id}/"
    return wagtail_request_handler(uri, params)


def page_details_by_uri(page_uri, params={}):
    uri = "pages/find/"
    params = params | {"html_path": page_uri}
    return wagtail_request_handler(uri, params)


def page_children(page_id, params={}):
    uri = "pages/"
    params = params | {"child_of": page_id}
    return wagtail_request_handler(uri, params)


def page_ancestors(page_id, params={}):
    uri = "pages/"
    params = params | {"ancestor_of": page_id}
    return wagtail_request_handler(uri, params)


def page_children_paginated(page_id, page, children_per_page, params={}):
    offset = (page - 1) * children_per_page
    uri = "pages/"
    order = "-first_published_at"
    params = params | {
        "child_of": page_id,
        "offset": offset,
        "limit": children_per_page,
        "order": order,
    }
    return wagtail_request_handler(uri, params)


# def image_details(image_id, params={}):
#     uri = f"images/{image_id}/"
#     return wagtail_request_handler(uri, params)


# def media_details(media_id, params={}):
#     uri = f"media/{media_id}/"
#     return wagtail_request_handler(uri, params)


def page_preview(content_type, token, params={}):
    uri = "page_preview/1/"
    params = params | {"content_type": content_type, "token": token}
    return wagtail_request_handler(uri, params)
