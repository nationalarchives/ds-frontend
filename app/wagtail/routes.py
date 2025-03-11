from urllib.parse import quote, unquote

from app.lib.api import ResourceNotFound
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

from .api import page_details, page_details_by_uri, page_preview


@bp.route("/preview/")
def preview_page():
    content_type = request.args.get("content_type")
    token = request.args.get("token")
    if content_type and token:
        try:
            page_data = page_preview(content_type, token)
        except ResourceNotFound:
            return render_template("errors/page_not_found.html"), 404
        except Exception as e:
            current_app.logger.error(f"Failed to render page preview: {e}")
            return render_template("errors/api.html"), 502
        return render_content_page(
            page_data | {"page_preview": True, "id": objects.get(page_data, "id", 0)}
        )
    return render_template("errors/page_not_found.html"), 404


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
    if path := objects.get(page_data, "meta.url").strip("/"):
        return redirect(
            url_for("wagtail.page", path=path),
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
        return CachedResponse(
            response=make_response(render_template("errors/page_not_found.html"), 404),
            timeout=1,
        )
    except Exception as e:
        current_app.logger.error(f"Failed to render page {path}: {e}")
        return CachedResponse(
            response=make_response(render_template("errors/api.html"), 502),
            timeout=1,
        )
    if "meta" not in page_data:
        current_app.logger.error(f"Page meta information not included for path: {path}")
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
    if objects.get(page_data, "meta.alias_of") and current_app.config.get(
        "REDIRECT_ALIASES"
    ):
        rediect_path = objects.get(page_data, "meta.alias_of.url", "").strip("/")
        if not rediect_path:
            current_app.logger.error(
                f"URL not found in alias page {page_data['id']}: {path}"
            )
        return redirect(
            url_for("wagtail.page", path=rediect_path),
            code=302,
        )
    if current_app.config.get("APPLY_REDIRECTS") and (
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
