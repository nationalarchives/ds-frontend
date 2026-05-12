from urllib.parse import unquote

from flask import current_app
from pydash import objects

from app.lib.api import JSONAPIClient


def wagtail_request_handler(uri, params=None):
    if params is None:
        params = {}
    api_url = current_app.config["WAGTAIL_API_URL"]
    if not api_url:
        current_app.logger.critical("WAGTAIL_API_URL not set")
        raise Exception("WAGTAIL_API_URL not set")
    default_headers = {}
    if api_key := current_app.config["WAGTAIL_API_KEY"]:
        default_headers["Authorization"] = f"Token {api_key}"
    default_params = {"format": "json"}
    client = JSONAPIClient(
        api_url, default_headers=default_headers, default_params=default_params
    )
    if site_hostname := current_app.config["WAGTAIL_SITE_HOSTNAME"]:
        client.add_parameter("site", site_hostname)
    client.add_parameters(params)
    return client.get(uri)


def breadcrumbs(page_id):
    if not page_id:
        return []
    ancestors = page_ancestors(page_id, params={"order": "depth"})
    return [
        {
            "text": (
                "Home"
                if objects.get(ancestor, "url") == "/"
                else (
                    objects.get(ancestor, "short_title")
                    or objects.get(ancestor, "title")
                )
            ),
            "href": objects.get(ancestor, "url"),
        }
        for ancestor in objects.get(ancestors, "items", [])
    ]


def all_pages(params=None, batch=1, limit=None):
    if params is None:
        params = {}
    if not limit:
        limit = current_app.config["WAGTAILAPI_LIMIT_MAX"]
    offset = (batch - 1) * limit
    params = params | {"offset": offset, "limit": limit}
    uri = "pages/"
    return wagtail_request_handler(uri, params)


def page_details(page_id, params=None):
    if params is None:
        params = {}
    uri = f"pages/{page_id}/"
    params = params | {
        "include_aliases": "",
    }
    return wagtail_request_handler(uri, params)


def page_details_by_uri(page_uri, params=None):
    if params is None:
        params = {}
    uri = "pages/find/"
    params = params | {
        "html_path": page_uri,
        "include_aliases": "",
    }
    return wagtail_request_handler(uri, params)


def page_details_by_type(page_type, params=None):
    if params is None:
        params = {}
    uri = "pages/"
    params = params | {
        "type": page_type,
        "include_aliases": "",
    }
    return wagtail_request_handler(uri, params)


def page_preview(content_type, token, params=None):
    if params is None:
        params = {}
    uri = "page_preview/1/"
    params = params | {"content_type": content_type, "token": token}
    return wagtail_request_handler(uri, params)


def page_children(page_id, params=None, limit=None):
    if params is None:
        params = {}
    if not page_id:
        return {}
    uri = "pages/"
    params = params | {
        "child_of": page_id,
        "limit": limit or current_app.config["WAGTAILAPI_LIMIT_MAX"],
        "include_aliases": "",
    }
    return wagtail_request_handler(uri, params)


def page_ancestors(page_id, params=None, limit=None):
    if params is None:
        params = {}
    if not page_id:
        return {}
    uri = "pages/"
    params = params | {
        "ancestor_of": page_id,
        "limit": limit or current_app.config["WAGTAILAPI_LIMIT_MAX"],
        "include_aliases": "",
    }
    try:
        return wagtail_request_handler(uri, params)
    except Exception:
        current_app.logger.exception(f"Failed to get ancestors for page {page_id}")
        return {}


def page_descendants(page_id, params=None, limit=None):
    if params is None:
        params = {}
    if not page_id:
        return {}
    uri = "pages/"
    params = params | {
        "descendant_of": page_id,
        "limit": limit or current_app.config["WAGTAILAPI_LIMIT_MAX"],
        "include_aliases": "",
    }
    try:
        return wagtail_request_handler(uri, params)
    except Exception:
        current_app.logger.exception(f"Failed to get decendants for page {page_id}")
        return {}


def pages_paginated(
    page,
    limit=None,
    initial_offset=0,
    params=None,
):
    if params is None:
        params = {}
    if not limit:
        limit = current_app.config["WAGTAILAPI_LIMIT_MAX"]
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
    params=None,
):
    if params is None:
        params = {}
    if not page_id:
        return {}
    return pages_paginated(
        page=page,
        limit=limit,
        initial_offset=initial_offset,
        params=params
        | {
            "child_of": page_id,
        },
    )


def authored_pages_paginated(
    author_id,
    page,
    limit=None,
    params=None,
):
    if params is None:
        params = {}
    return pages_paginated(
        page=page,
        limit=limit,
        params=params
        | {
            "author": author_id,
        },
    )


def media(media_uuid, params=None):
    if params is None:
        params = {}
    uri = f"media/{media_uuid}/"
    return wagtail_request_handler(uri, params)


def image(image_uuid, params=None):
    if params is None:
        params = {}
    uri = f"images/{image_uuid}/"
    return wagtail_request_handler(uri, params)


def redirect_by_uri(path, params=None):
    if params is None:
        params = {}
    uri = "redirects/find/"
    params = params | {
        "html_path": unquote(path),
    }
    return wagtail_request_handler(uri, params)


def blogs(params=None):
    if params is None:
        params = {}
    uri = "blogs/"
    return wagtail_request_handler(uri, params)


def blog_index(params=None):
    if params is None:
        params = {}
    uri = "blogs/index/"
    return wagtail_request_handler(uri, params)


def top_blogs(params=None):
    if params is None:
        params = {}
    uri = "blogs/top/"
    try:
        return wagtail_request_handler(uri, params)
    except Exception:
        current_app.logger.exception("Failed to get all blogs")
        return []


def blog_posts_paginated(
    page,
    blog_id=None,
    year=None,
    month=None,
    author=None,
    limit=None,
    initial_offset=0,
    order="-published_date",
    params=None,
):
    if params is None:
        params = {}
    if not limit:
        limit = current_app.config["WAGTAILAPI_LIMIT_MAX"]
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
    params=None,
):
    if params is None:
        params = {}
    uri = "blog_posts/count/"
    params = params | {
        "year": year,
        "month": month,
        "author": author,
        "descendant_of": blog_id,
    }
    try:
        return wagtail_request_handler(uri, params)
    except Exception:
        current_app.logger.exception("Failed to get blog post counts")
        return []


def blog_authors(
    blog_id=None,
    params=None,
):
    if params is None:
        params = {}
    uri = "blog_posts/authors/"
    params = params | {
        "descendant_of": blog_id,
    }
    try:
        return wagtail_request_handler(uri, params)
    except Exception:
        current_app.logger.exception("Failed to get blog authors")
        return []


def authors_paginated(
    author_id,
    page,
    limit=None,
    params=None,
):
    if params is None:
        params = {}
    if not limit:
        limit = current_app.config["WAGTAILAPI_LIMIT_MAX"]
    offset = (page - 1) * limit
    uri = "authors/"
    params = params | {
        "author": author_id,
        "offset": offset,
        "limit": limit,
    }
    return wagtail_request_handler(uri, params)


def events(event_type=None, location=None, from_date=None, to_date=None, params=None):
    if params is None:
        params = {}
    uri = "events/"
    if event_type:
        params = params | {"type": event_type}
    if location == "at_tna":
        params = params | {"at_tna": True}
    elif location == "online":
        params = params | {"online": True}
    if from_date:
        params = params | {"from": from_date}
    if to_date:
        params = params | {"to": to_date}
    params = params | {"order": "start_date"}
    return wagtail_request_handler(uri, params)


def global_alerts():
    try:
        home_page_alerts = page_details_by_uri(
            "/", {"fields": "_,global_alert,mourning_notice"}
        )
        global_alerts_data = {"mourning_notice": home_page_alerts["mourning_notice"]}
        if objects.get(home_page_alerts, "global_alert.cascade"):
            global_alerts_data["global_alert"] = home_page_alerts["global_alert"]
        return global_alerts_data
    except Exception:
        current_app.logger.exception("Failed to get global alerts")
        return None


def search(query, page, limit=None, params=None):
    if params is None:
        params = {}
    if not limit:
        limit = current_app.config["WAGTAILAPI_LIMIT_MAX"]
    offset = (page - 1) * limit
    uri = "pages/"
    params = params | {
        "offset": offset,
        "limit": limit,
    }
    params = params | {"search": query} if query else params | {"order": "-id"}
    return wagtail_request_handler(uri, params)


def foi_requests(
    page,
    limit=None,
    params=None,
):
    if params is None:
        params = {}
    if not limit:
        limit = current_app.config["WAGTAILAPI_LIMIT_MAX"]
    offset = (page - 1) * limit
    uri = "foi/"
    params = params | {"offset": offset, "limit": limit, "order": "-date,reference"}
    return wagtail_request_handler(uri, params)
