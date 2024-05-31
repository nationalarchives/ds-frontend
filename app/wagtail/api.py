import json
import os

import requests
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
    print(url)
    r = requests.get(url)
    if r.status_code == 404:
        current_app.logger.error(f"Resource not found: {url}")
        raise Exception("Resource not found")
    if r.status_code == requests.codes.ok:
        try:
            # if current_app.config["ENVIRONMENT"] == "staging":
            #     text = r.text
            #     text = text.replace(
            #         "https://main-bvxea6i-ncoml7u56y47e.uk-1.platformsh.site/",
            #         "https://main-bvxea6i-ncoml7u56y47e.uk-1.platformsh.site/",
            #     ).replace(
            #         "https://develop-sr3snxi-rasrzs7pi6sd4.uk-1.platformsh.site/",
            #         "https://main-bvxea6i-ncoml7u56y47e.uk-1.platformsh.site/",
            #     )
            #     return json.loads(text)
            # if current_app.config["ENVIRONMENT"] == "develop":
            #     text = r.text
            #     text = text.replace(
            #         "https://main-bvxea6i-ncoml7u56y47e.uk-1.platformsh.site/",
            #         "http://localhost:65535/",
            #     ).replace(
            #         "https://develop-sr3snxi-rasrzs7pi6sd4.uk-1.platformsh.site/",
            #         "http://localhost:65535/",
            #     )
            #     return json.loads(text)
            return r.json()
        except requests.exceptions.JSONDecodeError:
            current_app.logger.error("API provided non-JSON response")
            raise ConnectionError("API provided non-JSON response")
    current_app.logger.error(
        f"API responded with {r.status_code} status for {url}"
    )
    print("no conn")
    raise ConnectionError("Request to API failed")


def breadcrumbs(page_id):
    ancestors = page_ancestors(page_id)
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


def image_details(image_id, params={}):
    uri = f"images/{image_id}/"
    return wagtail_request_handler(uri, params)


def media_details(media_id, params={}):
    uri = f"media/{media_id}/"
    return wagtail_request_handler(uri, params)


def page_preview(content_type, token, params={}):
    uri = "page_preview/1/"
    params = params | {"content_type": content_type, "token": token}
    return wagtail_request_handler(uri, params)
