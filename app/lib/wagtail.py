import requests
from config import config
from flask import current_app


def wagtail_request_handler(uri):
    api_url = config["WAGTAIL_API_URL"].strip("/")
    r = requests.get(f"{api_url}/{uri}")
    if r.status_code == 404:
        raise Exception("Resource not found")
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
    uri = f"pages/find/?html_path={page_uri}"
    return wagtail_request_handler(uri)


def page_children(page_id):
    uri = f"pages/?child_of={page_id}"
    return wagtail_request_handler(uri)


def page_ancestors(page_id):
    uri = f"pages/?ancestor_of={page_id}"
    return wagtail_request_handler(uri)


def page_children_paginated(page_id, page, children_per_page):
    offset = (page - 1) * children_per_page
    uri = f"pages/?child_of={page_id}&offset={offset}&limit={children_per_page}"
    return wagtail_request_handler(uri)


def image_details(image_id):
    uri = f"images/{image_id}/"
    return wagtail_request_handler(uri)


def page_preview(content_type, token):
    uri = (
        f"page_preview/1/?content_type={content_type}&token={token}&format=json"
    )
    return wagtail_request_handler(uri)
