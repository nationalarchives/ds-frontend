import math
from urllib.parse import quote, unquote, urlparse

from app.lib.api import ResourceForbidden, ResourceNotFound
from app.lib.pagination import pagination_object
from app.wagtail import bp
from app.wagtail.api import global_alerts, search
from app.wagtail.render import render_content_page
from flask import (
    current_app,
    redirect,
    render_template,
    request,
    url_for,
)
from pydash import objects

from .api import (
    image,
    media,
    page_details,
    page_details_by_uri,
    page_preview,
    redirect_by_uri,
)


@bp.route("/preview/")
def preview_page():
    content_type = request.args.get("content_type")
    token = request.args.get("token")
    if not content_type or not token:
        return render_template("errors/page_not_found.html"), 404
    try:
        page_data = page_preview(content_type, token)
    except ResourceNotFound:
        return render_template("errors/page_not_found.html"), 404
    except ResourceForbidden:
        return render_template("errors/forbidden.html"), 403
    except Exception as e:
        current_app.logger.error(f"Failed to get page preview data: {e}")
        return render_template("errors/api.html"), 502
    try:
        return render_content_page(
            page_data | {"page_preview": True, "id": objects.get(page_data, "id", 0)}
        )
    except Exception as e:
        current_app.logger.error(f"Failed to render page preview: {e}")
        return render_template("errors/api.html"), 502


@bp.route("/preview/<int:page_id>/", methods=["GET", "POST"])
def preview_protected_page(page_id):
    """
    Renders a preview of a Wagtail page that is password protected.
    """

    try:
        # Get the page details from Wagtail by its and include the provided password
        password = objects.get(request.form, "password", "")
        params = {"password": password}
        page_data = page_details(
            page_id=page_id,
            params=params,
        )
    except ResourceNotFound:
        return render_template("errors/page_not_found.html"), 404
    except ResourceForbidden:
        return render_template("errors/forbidden.html"), 403
    except Exception as e:
        current_app.logger.error(f"Failed to render page preview: {e}")
        return render_template("errors/api.html"), 502

    # Check if the page is password protected
    if objects.get(page_data, "meta.privacy") == "password":
        # If meta.locked is True then the page is still locked which means the password
        # is not correct
        if objects.get(page_data, "meta.locked"):
            if request.method == "POST" and "password" in request.form:
                if request.form["password"] == "":
                    page_data["error"] = "Enter a password"
                else:
                    page_data["error"] = "Incorrect password"

            # Render the password protected page template
            return render_template(
                "errors/password_protected.html",
                page_data=page_data,
            )

        # If the page is not password protected, render the protected page
        return render_content_page(page_data)

    # If the page is no longer password protected, redirect to the main page URL
    if url := objects.get(page_data, "meta.url"):
        return redirect(url, code=302)

    return render_template("errors/api.html"), 502


@bp.route("/page/<int:page_id>/")
def page_permalink(page_id):
    """
    Redirects to the Wagtail page by its ID, if it exists, acting as a permalink.
    """

    try:
        # Get the page details from Wagtail by its ID
        page_data = page_details(page_id)
    except ResourceNotFound:
        return render_template("errors/page_not_found.html"), 404
    except ResourceForbidden:
        return render_template("errors/forbidden.html"), 403
    except Exception as e:
        current_app.logger.error(f"Failed to get page details: {e}")
        return render_template("errors/api.html"), 502

    # If the page has a URL, redirect to it
    if url := objects.get(page_data, "meta.url"):
        return redirect(url, code=302)

    # If the page does not have a URL, log an error and return a 502 error page
    current_app.logger.error(f"Cannot generate permalink for page: {page_id}")
    return render_template("errors/api.html"), 502


@bp.route("/", defaults={"path": "/"})
@bp.route("/<path:path>/")
def page(path):
    """
    This function handles the majority of Wagtail page requests.

    Renders a Wagtail page by its path, or tries to redirect to an external redirection
    if the page does not exist. If the page is password protected, it redirects to the
    preview page where the user can enter the password.

    If the page has a URL that is different from the requested path, it redirects to
    the canonical URL, which covers internal redirects added in Wagtail and if the
    page is an alias of another page, it redirects to the canonical page.
    """

    try:
        # Get the page details from Wagtail by the requested URI
        page_data = page_details_by_uri(unquote(f"/{path}/"))
    except ResourceNotFound:
        # If no page is found, try to match the requested path with any of the external
        # redirects added in Wagtail
        if current_app.config.get("SERVE_WAGTAIL_EXTERNAL_REDIRECTIONS"):
            return try_external_redirect(path)
        return render_template("errors/page_not_found.html"), 404
    except ResourceForbidden:
        # In the unlikely case that the API returns a 403, show a forbidden error page
        return render_template("errors/forbidden.html"), 403
    except Exception as e:
        # If any other error occurs, log it and return a generic API error page
        # with a 502 status code
        current_app.logger.error(f"Failed to render page: {e}")
        return render_template("errors/api.html"), 502

    # If the page data does not contain meta information, return a 502 error
    # as it is not possible to render the page without it
    if "meta" not in page_data:
        current_app.logger.error("Page meta not available")
        return render_template("errors/api.html"), 502

    # If the page is password protected, redirect to the preview page
    if objects.get(page_data, "meta.privacy") == "password":
        return redirect(
            url_for(
                "wagtail.preview_protected_page",
                page_id=page_data["id"],
            ),
            code=302,
        )

    # We can redirect to an alias page to its canonical page if
    # REDIRECT_WAGTAIL_ALIAS_PAGES is set to True
    if rediect_url := objects.get(page_data, "meta.alias_of.url"):
        if current_app.config.get("REDIRECT_WAGTAIL_ALIAS_PAGES"):
            return redirect(rediect_url, code=302)

    # If the page has a URL that is different from the requested path, redirect to it
    # which covers internal redirects added in Wagtail
    if current_app.config.get("SERVE_WAGTAIL_PAGE_REDIRECTIONS") and (
        urlparse(objects.get(page_data, "meta.url")).path
        != urlparse(f"/{quote(path)}/").path
    ):
        rediect_url = objects.get(page_data, "meta.url")
        return redirect(quote(rediect_url), code=302)

    # Render the page
    return render_content_page(page_data)


def try_external_redirect(path):
    """
    Renders a video details page.
    """

    # Normalise the path to ensure it starts with a slash and does not end with one
    if not path.startswith("/"):
        path = "/" + path
    if path.endswith("/") and len(path) > 1:
        path = path[:-1]

    # Build a query string from the request arguments
    query_string_keys = request.args.keys()
    query_string = "&".join(
        [f"{key}={request.args.get(key)}" for key in sorted(query_string_keys)]
    )
    if query_string:
        path = f"{path}?{query_string}"

    try:
        # Attempt to get the redirect data by the requested path
        redirect_data = redirect_by_uri(path)
    except ResourceNotFound:
        return render_template("errors/page_not_found.html"), 404
    except Exception as e:
        current_app.logger.error(f"Failed to get redirect: {e}")
        return render_template("errors/api.html"), 502

    # Get the redirect destination and whether it is permanent
    rediect_destination = redirect_data.get("location", "/")
    is_permanent = redirect_data.get("is_permanent", False)

    # Return the redirect to the user
    return redirect(
        rediect_destination,
        code=(301 if is_permanent else 302),
    )


@bp.route("/video/<uuid:media_uuid>/")
def media_page(media_uuid):
    """
    Renders a video details page.
    """

    try:
        media_data = media(media_uuid=media_uuid)
    except ResourceNotFound:
        return render_template("errors/page_not_found.html"), 404
    except ResourceForbidden:
        return render_template("errors/forbidden.html"), 403
    except Exception as e:
        current_app.logger.error(f"Failed to get video: {e}")
        return render_template("errors/api.html"), 502
    return render_template("media/video.html", media_data=media_data)


@bp.route("/image/<uuid:image_uuid>/")
def image_page(image_uuid):
    """
    Renders an image details page.
    """

    try:
        image_data = image(image_uuid=image_uuid)
    except ResourceNotFound:
        return render_template("errors/page_not_found.html"), 404
    except ResourceForbidden:
        return render_template("errors/forbidden.html"), 403
    except Exception as e:
        current_app.logger.error(f"Failed to get video: {e}")
        return render_template("errors/api.html"), 502
    return render_template("media/image.html", image_data=image_data)


@bp.route("/explore-the-collection/search/")
def search_explore_the_collection():
    """
    Show a search page for the Explore the collection section with a fixed URL.

    In the future, this might be added to Wagtail as a customisable search page
    """

    children_per_page = 12
    page = (
        int(request.args.get("page"))
        if request.args.get("page") and request.args.get("page").isnumeric()
        else 1
    )
    query = unquote(request.args.get("q", "")).strip(" ")
    existing_qs_as_dict = request.args.to_dict()
    params = {"descendant_of_path": "/explore-the-collection/"}
    order = request.args.get("order", "relevance")
    if order == "date":
        params = params | {"order": "-first_published_at"}
    elif order != "relevance":
        params = params | {"order": order}
    results = search(
        query=query,
        page=page,
        limit=children_per_page,
        params=params,
    )
    total_results = objects.get(results, "meta.total_count", 0)
    pages = math.ceil(total_results / children_per_page)
    if pages > 0 and page > pages:
        return render_template("errors/page_not_found.html"), 404
    return render_template(
        "explore_the_collection/search.html",
        q=query,
        existing_qs=existing_qs_as_dict,
        global_alert=global_alerts(),
        results=results,
        page=page,
        pages=pages,
        children_per_page=children_per_page,
        total_results=total_results,
        pagination=pagination_object(page, pages, request.args),
    )
