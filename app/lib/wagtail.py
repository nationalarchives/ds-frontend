import requests
from config import config
from flask import current_app


def wagtail_request_handler(uri):
    r = requests.get("%s/%s" % (config["WAGTAIL_API_URL"].strip("/"), uri))
    if r.status_code == 404:
        raise Exception("Resource not found")
    if r.status_code == requests.codes.ok:
        try:
            return r.json()
        except requests.exceptions.JSONDecodeError as e:
            current_app.logger.error(e)
            raise ConnectionError("API provided non-JSON response")
    current_app.logger.error("API responded with %d status" % r.status_code)
    raise ConnectionError("Request to API failed")


def page_details(page_id):
    uri = "pages/%d/" % page_id
    return wagtail_request_handler(uri)


def page_details_by_uri(page_uri):
    uri = "pages/find/?html_path=%s" % page_uri
    return wagtail_request_handler(uri)


def page_children(page_id):
    uri = "pages/?child_of=%d" % page_id
    return wagtail_request_handler(uri)


def page_children_paginated(page_id, page, children_per_page):
    uri = "pages/?child_of=%d&offset=%d&limit=%d" % (
        page_id,
        (page - 1) * children_per_page,
        children_per_page,
    )
    return wagtail_request_handler(uri)


def image_details(image_id):
    uri = "images/%d/" % image_id
    return wagtail_request_handler(uri)
