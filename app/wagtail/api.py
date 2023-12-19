import os
import requests
from config import Config
from flask import current_app


def wagtail_request_handler(uri, params={}):
    api_url = Config().WAGTAIL_API_URL.strip("/")
    params["format"] = "json"
    query_string = "&".join(
        ["=".join((str(key), str(value))) for key, value in params.items()]
    )
    url = f"{api_url}/{uri}?{query_string}"
    r = requests.get(url)
    if r.status_code == 404:
        # print(url)
        # print("404")
        raise Exception("Resource not found")
        return {}
    if r.status_code == requests.codes.ok:
        try:
            if os.environ.get("ENVIRONMENT") == "develop" or os.environ.get("ENVIRONMENT") == "staging":
                r = r.replace("https://develop-sr3snxi-rasrzs7pi6sd4.uk-1.platformsh.site/", "http://localhost:65535/")
                r = r.replace("http://localhost:8000/", "http://localhost:65535/")
                r = r.replace("http://127.0.0.1:8000/", "http://localhost:65535/")
            return r.json()
        except requests.exceptions.JSONDecodeError as e:
            # print("no JSON")
            current_app.logger.error(e)
            raise ConnectionError("API provided non-JSON response")
    current_app.logger.error(f"API responded with {r.status_code} status")
    # print("no conn")
    raise ConnectionError("Request to API failed")


def breadcrumbs(page_id):
    ancestors = page_ancestors(page_id)
    return (
        [
            {
                "text": "Home"
                if ancestor["meta"]["type"] == "home.HomePage"
                else ancestor["title"],
                "href": ancestor["meta"]["html_url"],
            }
            for ancestor in ancestors["items"]
        ]
        if ancestors
        else []
    )


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


def media_details(media_id):
    uri = f"media/{media_id}/"
    return wagtail_request_handler(uri)


def page_preview(content_type, token):
    uri = "page_preview/1/"
    params = {"content_type": content_type, "token": token}
    return wagtail_request_handler(uri, params)
