from urllib.parse import quote, unquote

from app.lib.api import ResourceForbidden, ResourceNotFound
from app.lib.cache import cache, page_cache_key_prefix
from app.wagtail import bp
from app.wagtail.render import render_content_page
from flask import (
    current_app,
    make_response,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_caching import CachedResponse
from pydash import objects

from .api import media, page_details, page_details_by_uri, page_preview, redirect_by_uri


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
    try:
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
    if objects.get(page_data, "meta.privacy") == "password":
        if objects.get(page_data, "meta.locked"):
            if request.method == "POST" and "password" in request.form:
                if request.form["password"] == "":
                    page_data["error"] = "Enter a password"
                else:
                    page_data["error"] = "Incorrect password"
            return render_template(
                "errors/password_protected.html",
                page_data=page_data,
            )
        return render_content_page(page_data)
    if path := objects.get(page_data, "meta.url"):
        return redirect(
            url_for("wagtail.page", path=path.strip("/")),
            code=302,
        )
    return render_template("errors/api.html"), 502


@bp.route("/page/<int:page_id>/")
@cache.cached(key_prefix=page_cache_key_prefix)
def page_permalink(page_id):
    try:
        page_data = page_details(page_id)
    except ResourceNotFound:
        return render_template("errors/page_not_found.html"), 404
    except ResourceForbidden:
        return render_template("errors/forbidden.html"), 403
    except Exception as e:
        current_app.logger.error(f"Failed to get page details: {e}")
        return render_template("errors/api.html"), 502
    if path := objects.get(page_data, "meta.url"):
        return redirect(
            url_for(
                "wagtail.page",
                path=path.strip("/"),
                **request.args.to_dict(),
            ),
            code=302,
        )
    current_app.logger.error(f"Cannot generate permalink for page: {page_id}")
    return CachedResponse(
        response=make_response(render_template("errors/api.html"), 502),
        timeout=1,
    )


@bp.route("/")
@cache.cached(key_prefix=page_cache_key_prefix)
def index():
    try:
        page_data = page_details_by_uri("/")
    except ResourceNotFound:
        return CachedResponse(
            response=make_response(render_template("errors/page_not_found.html"), 404),
            timeout=1,
        )
    except ResourceForbidden:
        return CachedResponse(
            response=make_response(render_template("errors/forbidden.html"), 403),
            timeout=1,
        )
    except Exception as e:
        current_app.logger.error(f"Failed to render the home page: {e}")
        return CachedResponse(
            response=make_response(render_template("errors/api.html"), 502),
            timeout=1,
        )
    return CachedResponse(
        response=make_response(render_content_page(page_data)),
        timeout=current_app.config.get("CACHE_DEFAULT_TIMEOUT"),
    )


@bp.route("/<path:path>/")
@cache.cached(key_prefix=page_cache_key_prefix)
def page(path):
    try:
        page_data = page_details_by_uri(unquote(f"/{path}/"))
    except ResourceNotFound:
        if current_app.config.get("SERVE_WAGTAIL_EXTERNAL_REDIRECTIONS"):
            return try_external_redirect(path)
        return CachedResponse(
            response=make_response(render_template("errors/page_not_found.html"), 404),
            timeout=1,
        )
    except ResourceForbidden:
        return CachedResponse(
            response=make_response(render_template("errors/forbidden.html"), 403),
            timeout=1,
        )
    except Exception as e:
        current_app.logger.error(f"Failed to render page: {e}")
        return CachedResponse(
            response=make_response(render_template("errors/api.html"), 502),
            timeout=1,
        )
    if "meta" not in page_data:
        current_app.logger.error("Page meta not available")
        return CachedResponse(
            response=make_response(render_template("errors/api.html"), 502),
            timeout=1,
        )
    if objects.get(page_data, "meta.privacy") == "password":
        return redirect(
            url_for(
                "wagtail.preview_protected_page",
                page_id=page_data["id"],
            ),
            code=302,
        )
    if rediect_path := objects.get(page_data, "meta.alias_of.url"):
        if current_app.config.get("REDIRECT_WAGTAIL_ALIAS_PAGES"):
            return redirect(
                url_for("wagtail.page", path=rediect_path.strip("/")),
                code=302,
            )
    if current_app.config.get("SERVE_WAGTAIL_PAGE_REDIRECTIONS") and (
        quote(objects.get(page_data, "meta.url")) != quote(f"/{path}/")
    ):
        rediect_path = objects.get(page_data, "meta.url").strip("/")
        return redirect(
            url_for("wagtail.page", path=rediect_path),
            code=302,
        )
    return CachedResponse(
        response=make_response(render_content_page(page_data)),
        timeout=current_app.config.get("CACHE_DEFAULT_TIMEOUT"),
    )


def try_external_redirect(path):
    if not path.startswith("/"):
        path = "/" + path
    if path.endswith("/") and len(path) > 1:
        path = path[:-1]
    query_string_keys = request.args.keys()
    query_string = "&".join(
        [f"{key}={request.args.get(key)}" for key in sorted(query_string_keys)]
    )
    if query_string:
        path = f"{path}?{query_string}"
    try:
        redirect_data = redirect_by_uri(path)
    except ResourceNotFound:
        return render_template("errors/page_not_found.html"), 404
    except Exception as e:
        current_app.logger.error(f"Failed to get redirect: {e}")
        return render_template("errors/api.html"), 502
    rediect_destination = redirect_data.get("location", "/")
    is_permanent = redirect_data.get("is_permanent", False)
    return redirect(
        rediect_destination,
        code=(301 if is_permanent else 302),
    )


@bp.route("/video/<int:video_id>-<string:video_title>/")
@cache.cached(key_prefix=page_cache_key_prefix)
def video_page(video_id, video_title):
    try:
        video_data = media(media_id=video_id)
    except ResourceNotFound:
        return CachedResponse(
            response=make_response(render_template("errors/page_not_found.html"), 404),
            timeout=1,
        )
    except ResourceForbidden:
        return CachedResponse(
            response=make_response(render_template("errors/forbidden.html"), 403),
            timeout=1,
        )
    except Exception as e:
        current_app.logger.error(f"Failed to get video: {e}")
        return CachedResponse(
            response=make_response(render_template("errors/api.html"), 502),
            timeout=1,
        )
    if video_data.get("title") != video_title:
        return CachedResponse(
            response=make_response(render_template("errors/page_not_found.html"), 404),
            timeout=1,
        )
    
    return CachedResponse(
        response=make_response(
            render_template("media/video.html", video_data=video_data)
        ),
        timeout=current_app.config.get("CACHE_DEFAULT_TIMEOUT"),
    )
