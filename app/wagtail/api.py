import asyncio
from urllib.parse import unquote

import aiohttp
from app.lib.api import ResourceForbidden, ResourceNotFound
from flask import current_app
from pydash import objects

_RAISE = object()
_UNRESOLVED = object()


class WagtailRequest:
    """A deferred Wagtail API request that can be executed in a batch."""

    def __init__(self, uri, params=None, default=_RAISE):
        self.uri = uri
        self.params = params or {}
        self.default = default
        self._resolved = _UNRESOLVED

    def with_default(self, default):
        """Set a default value to return on error instead of raising."""
        self.default = default
        return self

    @staticmethod
    def resolved(value):
        """Create a pre-resolved request that returns a fixed value."""
        req = WagtailRequest.__new__(WagtailRequest)
        req.uri = None
        req.params = {}
        req.default = _RAISE
        req._resolved = value
        return req

    @property
    def is_resolved(self):
        return self._resolved is not _UNRESOLVED


async def _fetch_one(session, base_url, headers, wagtail_request):
    """Fetch a single request using the shared aiohttp session."""
    if wagtail_request.is_resolved:
        return wagtail_request._resolved

    url = f"{base_url}/{wagtail_request.uri.lstrip('/')}"
    status_errors = {
        400: lambda s: Exception("Bad request"),
        403: lambda s: ResourceForbidden("Forbidden"),
        404: lambda s: ResourceNotFound("Resource not found"),
    }
    try:
        async with session.get(
            url, params=wagtail_request.params, headers=headers
        ) as response:
            if response.status == 200:
                try:
                    return await response.json()
                except Exception:
                    raise Exception("Non-JSON response provided")
            error_factory = status_errors.get(response.status)
            if error_factory:
                raise error_factory(response.status)
            raise Exception(f"Wagtail API responded with {response.status}")
    except (ResourceNotFound, ResourceForbidden, Exception) as e:
        if isinstance(e, (ResourceNotFound, ResourceForbidden)):
            raise
        if isinstance(e, aiohttp.ClientError):
            raise ConnectionError(f"A connection error occurred: {e}")
        if isinstance(e, asyncio.TimeoutError):
            raise ConnectionError("The request timed out")
        raise


async def _fetch_all(base_url, headers, requests):
    """Execute multiple requests concurrently using a single aiohttp session."""
    timeout = aiohttp.ClientTimeout(total=30)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        tasks = [_fetch_one(session, base_url, headers, req) for req in requests]
        return await asyncio.gather(*tasks, return_exceptions=True)


def fetch(*requests):
    """Execute one or more WagtailRequests in parallel using aiohttp.

    Returns results in the same order as the requests.
    A single request returns a single value; multiple requests return a tuple.
    """
    api_url = current_app.config["WAGTAIL_API_URL"]
    if not api_url:
        current_app.logger.critical("WAGTAIL_API_URL not set")
        raise Exception("WAGTAIL_API_URL not set")

    headers = {
        "Cache-Control": "no-cache",
        "Accept": "application/json",
    }
    if api_key := current_app.config["WAGTAIL_API_KEY"]:
        headers["Authorization"] = f"Token {api_key}"

    base_params = {"format": "json"}
    if site_hostname := current_app.config["WAGTAIL_SITE_HOSTNAME"]:
        base_params["site"] = site_hostname

    prepared = []
    for req in requests:
        if req.is_resolved:
            prepared.append(req)
        else:
            prepared.append(
                WagtailRequest(req.uri, base_params | req.params, req.default)
            )

    results = asyncio.run(_fetch_all(api_url, headers, prepared))

    processed = []
    for i, result in enumerate(results):
        if isinstance(result, BaseException):
            if requests[i].default is not _RAISE:
                current_app.logger.error(
                    f"Wagtail API error for {requests[i].uri}: {result}"
                )
                processed.append(requests[i].default)
            else:
                raise result
        else:
            processed.append(result)

    if len(processed) == 1:
        return processed[0]
    return tuple(processed)


def breadcrumbs(ancestors_data):
    """Process ancestors data into breadcrumb format."""
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
        for ancestor in objects.get(ancestors_data, "items", [])
    ]


def all_pages(params={}, batch=1, limit=None):
    if not limit:
        limit = current_app.config["WAGTAILAPI_LIMIT_MAX"]
    offset = (batch - 1) * limit
    return WagtailRequest("pages/", params | {"offset": offset, "limit": limit})


def page_details(page_id, params={}):
    return WagtailRequest(f"pages/{page_id}/", params | {"include_aliases": ""})


def page_details_by_uri(page_uri, params={}):
    return WagtailRequest(
        "pages/find/",
        params | {"html_path": page_uri, "include_aliases": ""},
    )


def page_details_by_type(type, params={}):
    return WagtailRequest("pages/", params | {"type": type, "include_aliases": ""})


def page_preview(content_type, token, params={}):
    return WagtailRequest(
        "page_preview/1/",
        params | {"content_type": content_type, "token": token},
    )


def page_children(page_id, params={}, limit=None):
    if not page_id:
        return WagtailRequest.resolved({})
    return WagtailRequest(
        "pages/",
        params
        | {
            "child_of": page_id,
            "limit": limit or current_app.config["WAGTAILAPI_LIMIT_MAX"],
            "include_aliases": "",
        },
    )


def page_ancestors(page_id, params={}, limit=None):
    if not page_id:
        return WagtailRequest.resolved({})
    return WagtailRequest(
        "pages/",
        params
        | {
            "ancestor_of": page_id,
            "limit": limit or current_app.config["WAGTAILAPI_LIMIT_MAX"],
            "include_aliases": "",
        },
        default={},
    )


def page_descendants(page_id, params={}, limit=None):
    if not page_id:
        return WagtailRequest.resolved({})
    return WagtailRequest(
        "pages/",
        params
        | {
            "descendant_of": page_id,
            "limit": limit or current_app.config["WAGTAILAPI_LIMIT_MAX"],
            "include_aliases": "",
        },
        default={},
    )


def pages_paginated(
    page,
    limit=None,
    initial_offset=0,
    params={},
):
    if not limit:
        limit = current_app.config["WAGTAILAPI_LIMIT_MAX"]
    offset = ((page - 1) * limit) + initial_offset
    return WagtailRequest("pages/", params | {"offset": offset, "limit": limit})


def page_children_paginated(
    page_id,
    page,
    limit=None,
    initial_offset=0,
    params={},
):
    if not page_id:
        return WagtailRequest.resolved({})
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
    params={},
):
    return pages_paginated(
        page=page,
        limit=limit,
        params=params
        | {
            "author": author_id,
        },
    )


def media(media_uuid, params={}):
    return WagtailRequest(f"media/{media_uuid}/", params)


def image(image_uuid, params={}):
    return WagtailRequest(f"images/{image_uuid}/", params)


def redirect_by_uri(path, params={}):
    return WagtailRequest("redirects/find/", params | {"html_path": unquote(path)})


def blogs(params={}):
    return WagtailRequest("blogs/", params)


def blog_index(params={}):
    return WagtailRequest("blogs/index/", params)


def top_blogs(params={}):
    return WagtailRequest("blogs/top/", params, default=[])


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
    if blog_id is not None:
        params = params | {"descendant_of": blog_id}
    if year is not None:
        params = params | {"year": year}
    if month is not None:
        params = params | {"month": month}
    if author is not None:
        params = params | {"author": author}
    if not limit:
        limit = current_app.config["WAGTAILAPI_LIMIT_MAX"]
    offset = ((page - 1) * limit) + initial_offset
    params = params | {"order": order, "limit": limit, "offset": offset}
    return WagtailRequest(
        "blog_posts/",
        params,
    )


def blog_post_counts(
    blog_id=None,
    year=None,
    month=None,
    author=None,
    params={},
):
    if blog_id is not None:
        params = params | {"descendant_of": blog_id}
    if year is not None:
        params = params | {"year": year}
    if month is not None:
        params = params | {"month": month}
    if author is not None:
        params = params | {"author": author}
    return WagtailRequest(
        "blog_posts/count/",
        params,
        default=[],
    )


def blog_authors(
    blog_id=None,
    params={},
):
    if blog_id is not None:
        params = params | {"descendant_of": blog_id}
    return WagtailRequest(
        "blog_posts/authors/",
        params,
        default=[],
    )


def authors_paginated(
    author_id,
    page,
    limit=None,
    params={},
):
    if not limit:
        limit = current_app.config["WAGTAILAPI_LIMIT_MAX"]
    offset = (page - 1) * limit
    params = params | {"author": author_id, "offset": offset, "limit": limit}
    return WagtailRequest(
        "authors/",
        params,
    )


def events(type=None, location=None, from_date=None, to_date=None, params={}):
    if type:
        params = params | {"type": type}
    if location == "at_tna":
        params = params | {"at_tna": True}
    elif location == "online":
        params = params | {"online": True}
    if from_date:
        params = params | {"from": from_date}
    if to_date:
        params = params | {"to": to_date}
    params = params | {"order": "start_date"}
    return WagtailRequest("events/", params)


def global_alerts_request():
    """Create a request for global alerts data."""
    return page_details_by_uri(
        "/", {"fields": "_,global_alert,mourning_notice"}
    ).with_default(None)


def process_global_alerts(data):
    """Process raw global alerts data into the expected format."""
    if not data:
        return None
    try:
        global_alerts_data = {"mourning_notice": data["mourning_notice"]}
        if objects.get(data, "global_alert.cascade"):
            global_alerts_data["global_alert"] = data["global_alert"]
        return global_alerts_data
    except Exception:
        return None


def search(query, page, limit=None, params={}):
    if not limit:
        limit = current_app.config["WAGTAILAPI_LIMIT_MAX"]
    offset = (page - 1) * limit
    params = params | {
        "offset": offset,
        "limit": limit,
    }
    if query:
        params = params | {
            "search": query,
        }
    else:
        params = params | {
            "order": "-id",
        }
    return WagtailRequest("pages/", params)


def foi_requests(
    page,
    limit=None,
    params={},
):
    if not limit:
        limit = current_app.config["WAGTAILAPI_LIMIT_MAX"]
    offset = (page - 1) * limit
    params = params | {"offset": offset, "limit": limit, "order": "-date,reference"}
    return WagtailRequest(
        "foi/",
        params,
    )
