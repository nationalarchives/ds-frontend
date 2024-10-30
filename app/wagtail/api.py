from app.lib.api import ApiResourceNotFound, JSONAPIClient
from flask import current_app
from pydash import objects


def wagtail_request_handler(uri, params={}):
    api_url = current_app.config.get("WAGTAIL_API_URL")
    if not api_url:
        current_app.logger.critical("WAGTAIL_API_URL not set")
        raise Exception("WAGTAIL_API_URL not set")
    client = JSONAPIClient(api_url)
    client.add_parameter("format", "json")
    client.add_parameters(params)
    data = client.get(uri)
    return data


def breadcrumbs(page_id):
    try:
        ancestors = page_ancestors(page_id, params={"order": "depth"})
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


def page_details_by_type(type, params={}):
    uri = "pages/"
    params = params | {
        "type": type,
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


def pages_paginated(
    page,
    limit=None,
    initial_offset=0,
    params={},
):
    if not limit:
        limit = current_app.config.get("WAGTAILAPI_LIMIT_MAX")
    offset = ((page - 1) * limit) + initial_offset
    uri = "pages/"
    params = params | {
        "offset": offset,
        "limit": limit,
    }
    return wagtail_request_handler(uri, params)


def page_children_paginated(
    page_id,
    page,
    limit=None,
    initial_offset=0,
    params={},
):
    return pages_paginated(
        page=page,
        limit=limit,
        initial_offset=initial_offset,
        params=params | {"child_of": page_id},
    )


def page_descendants(
    page_id,
    params={},
):
    uri = "pages/"
    params = params | {"descendant_of": page_id}
    return wagtail_request_handler(uri, params)


def blogs(params={}):
    uri = "blogs/"
    return wagtail_request_handler(uri, params)


def blog_posts_paginated(
    page,
    blog_id=None,
    year=None,
    month=None,
    author=None,
    limit=None,
    initial_offset=0,
    order="-published_date",
    params={},
):
    if not limit:
        limit = current_app.config.get("WAGTAILAPI_LIMIT_MAX")
    offset = ((page - 1) * limit) + initial_offset
    uri = "blog_posts/"
    params = params | {
        "offset": offset,
        "limit": limit,
        "order": order,
        "year": year,
        "month": month,
        "author": author,
        "descendant_of": blog_id,
    }
    return wagtail_request_handler(uri, params)


def blog_post_counts(
    blog_id=None,
    year=None,
    month=None,
    author=None,
    params={},
):
    uri = "blog_posts/count/"
    params = params | {
        "year": year,
        "month": month,
        "author": author,
        "descendant_of": blog_id,
    }
    return wagtail_request_handler(uri, params)


def blog_authors(
    blog_id=None,
    params={},
):
    uri = "blog_posts/authors/"
    params = params | {
        "descendant_of": blog_id,
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
