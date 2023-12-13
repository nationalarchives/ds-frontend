import requests
from config import config
from flask import current_app


def wagtail_request_handler(uri, params={}):
    api_url = config["WAGTAIL_API_URL"].strip("/")
    params["format"] = "json"
    query_string = "&".join(
        ["=".join((str(key), str(value))) for key, value in params.items()]
    )
    r = requests.get(f"{api_url}/{uri}?{query_string}")
    if r.status_code == 404:
        # raise Exception("Resource not found")
        return {}
    if r.status_code == requests.codes.ok:
        try:
            return r.json()
        except requests.exceptions.JSONDecodeError as e:
            current_app.logger.error(e)
            raise ConnectionError("API provided non-JSON response")
    current_app.logger.error(f"API responded with {r.status_code} status")
    raise ConnectionError("Request to API failed")


def page_details(page_id):
    uri = f"pages/{page_id}/"
    return wagtail_request_handler(uri)


def page_details_by_uri(page_uri):
    uri = "pages/find/"
    params = {"html_path": page_uri}
    return wagtail_request_handler(uri, params)


def page_children(page_id):
    uri = "pages/"
    params = {"child_of": page_id}
    return wagtail_request_handler(uri, params)


def page_ancestors(page_id):
    uri = "pages/"
    params = {"ancestor_of": page_id}
    return wagtail_request_handler(uri, params)


def page_children_paginated(page_id, page, children_per_page):
    offset = (page - 1) * children_per_page
    uri = "pages/"
    order = "-first_published_at"
    params = {
        "child_of": page_id,
        "offset": offset,
        "limit": children_per_page,
        "order": order,
    }
    return wagtail_request_handler(uri, params)


def image_details(image_id):
    uri = f"images/{image_id}/"
    return wagtail_request_handler(uri)


def page_preview(content_type, token):
    uri = "page_preview/1/"
    params = {"content_type": content_type, "token": token}
    return wagtail_request_handler(uri, params)
