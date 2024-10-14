import requests
from app.lib.api import ApiResourceNotFound
from flask import current_app
from pydash import objects


def wagtail_request_handler(uri, params={}):
    api_url = current_app.config.get("WAGTAIL_API_URL")
    if not api_url:
        current_app.logger.critical("WAGTAIL_API_URL not set")
        raise Exception("WAGTAIL_API_URL not set")
    params["format"] = "json"
    url = f"{api_url}/{uri}"
    current_app.logger.debug(f"API endpoint requested: {url} (params {params})")
    r = requests.get(url, params=params)
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
        current_app.logger.warning(
            f"Failed to get ancestors for page {page_id}"
        )
        return []
    return (
        [
            {
                "text": (
                    "Home" if ancestor["url"] == "/" else ancestor["title"]
                ),
                "href": (ancestor["url"]),
            }
            for ancestor in ancestors["items"]
        ]
        if ancestors
        else []
    )


def all_pages(params={}, batch=1, limit=None):
    if not limit:
        limit = current_app.config.get("WAGTAILAPI_LIMIT_MAX")
    offset = (batch - 1) * limit
    params = params | {"offset": offset, "limit": limit}
    uri = "pages/"
    return wagtail_request_handler(uri, params)


def page_details(page_id, params={}):
    uri = f"pages/{page_id}/"
    return wagtail_request_handler(uri, params)


def page_details_by_uri(page_uri, params={}):
    uri = "pages/find/"
    params = params | {
        "html_path": page_uri,
    }
    return wagtail_request_handler(uri, params)


def page_children(page_id, params={}, limit=None):
    uri = "pages/"
    params = params | {
        "child_of": page_id,
        "limit": limit or current_app.config.get("WAGTAILAPI_LIMIT_MAX"),
    }
    return wagtail_request_handler(uri, params)


def page_ancestors(page_id, params={}, limit=None):
    uri = "pages/"
    params = params | {
        "ancestor_of": page_id,
        "limit": limit or current_app.config.get("WAGTAILAPI_LIMIT_MAX"),
    }
    return wagtail_request_handler(uri, params)


def page_children_paginated(
    page_id,
    page,
    limit=None,
    initial_offset=0,
    order="-first_published_at",
    params={},
):
    if not limit:
        limit = current_app.config.get("WAGTAILAPI_LIMIT_MAX")
    offset = ((page - 1) * limit) + initial_offset
    uri = "pages/"
    params = params | {
        "child_of": page_id,
        "offset": offset,
        "limit": limit,
        "order": order,
    }
    return wagtail_request_handler(uri, params)


def pages_by_type(types, order="-first_published_at", params={}):
    uri = "pages/"
    params = params | {
        "type": ",".join(types),
        "order": order,
    }
    return wagtail_request_handler(uri, params)


def pages_by_type_paginated(
    types,
    page,
    limit=None,
    initial_offset=0,
    order="-first_published_at",
    params={},
):
    if not limit:
        limit = current_app.config.get("WAGTAILAPI_LIMIT_MAX")
    offset = ((page - 1) * limit) + initial_offset
    uri = "pages/"
    params = params | {
        "type": ",".join(types),
        "offset": offset,
        "limit": limit,
        "order": order,
    }
    return wagtail_request_handler(uri, params)


def page_preview(content_type, token, params={}):
    uri = "page_preview/1/"
    params = params | {"content_type": content_type, "token": token}
    return wagtail_request_handler(uri, params)


def global_alerts():
    try:
        home_page_alerts = page_details_by_uri(
            "/", {"fields": "_,global_alert,mourning_notice"}
        )
        global_alerts_data = {
            "mourning_notice": home_page_alerts["mourning_notice"]
        }
        if objects.get(home_page_alerts, "global_alert.cascade"):
            global_alerts_data["global_alert"] = home_page_alerts[
                "global_alert"
            ]
        return global_alerts_data
    except ApiResourceNotFound:
        current_app.logger.warn(
            "Global alerts could not be retrieved (ApiResourceNotFound)"
        )
        return None
    except ConnectionError:
        current_app.logger.warn(
            "Global alerts could not be retrieved (ConnectionError)"
        )
        return None
    except Exception:
        current_app.logger.warn(
            "Global alerts could not be retrieved (Exception)"
        )
        return None
