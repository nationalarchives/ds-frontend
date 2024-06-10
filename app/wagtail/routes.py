from app.lib import cache, cache_key_prefix
from app.lib.api import ApiResourceNotFound
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

from .api import page_details, page_details_by_uri, page_preview


@bp.route("/preview/")
def preview_page():
    content_type = request.args.get("content_type")
    token = request.args.get("token")
    page_data = page_preview(content_type, token)
    return render_content_page(page_data | {"page_preview": True})


@bp.route("/preview/<int:id>/", methods=["GET", "POST"])
def preview_protected_page(id):
    try:
        page_data = page_details(
            id,
            {
                "password": (
                    request.form["password"]
                    if "password" in request.form
                    else ""
                )
            },
        )
    except ConnectionError:
        return CachedResponse(
            response=make_response(render_template("errors/api.html"), 502),
            timeout=1,
        )
    except ApiResourceNotFound:
        return CachedResponse(
            response=make_response(
                render_template("errors/page-not-found.html"), 404
            ),
            timeout=1,
        )
    except Exception:
        return CachedResponse(
            response=make_response(render_template("errors/api.html"), 502),
            timeout=1,
        )
    if "meta" in page_data:
        if (
            "privacy" in page_data["meta"]
            and page_data["meta"]["privacy"] == "password"
        ):
            if "locked" in page_data["meta"] and page_data["meta"]["locked"]:
                if request.method == "POST" and "password" in request.form:
                    if request.form["password"] == "":
                        page_data["error"] = "Enter a password"
                    else:
                        page_data["error"] = "Incorrect password"
                return CachedResponse(
                    response=make_response(
                        render_template(
                            "errors/password-protected.html",
                            page_data=page_data,
                        )
                    ),
                    timeout=1,
                )
            return CachedResponse(
                response=make_response(render_content_page(page_data)),
                timeout=current_app.config["CACHE_DEFAULT_TIMEOUT"],
            )
        if "url" in page_data["meta"]:
            return redirect(
                url_for("wagtail.page", path=page_data["meta"]["url"]),
                code=302,
            )
    return CachedResponse(
        response=make_response(render_template("errors/api.html"), 502),
        timeout=1,
    )


@bp.route("/")
@cache.cached(key_prefix=cache_key_prefix)
def index():
    try:
        page_data = page_details_by_uri("/")
    except ConnectionError:
        return CachedResponse(
            response=make_response(render_template("errors/api.html"), 502),
            timeout=1,
        )
    except ApiResourceNotFound:
        return CachedResponse(
            response=make_response(
                render_template("errors/page-not-found.html"), 404
            ),
            timeout=1,
        )
    except Exception:
        return CachedResponse(
            response=make_response(render_template("errors/api.html"), 502),
            timeout=1,
        )
    return CachedResponse(
        response=make_response(render_content_page(page_data)),
        timeout=current_app.config["CACHE_DEFAULT_TIMEOUT"],
    )


@bp.route("/<path:path>/")
@cache.cached(key_prefix=cache_key_prefix)
def page(path):
    try:
        page_data = page_details_by_uri(path)
    except ConnectionError:
        return CachedResponse(
            response=make_response(render_template("errors/api.html"), 502),
            timeout=1,
        )
    except ApiResourceNotFound:
        return CachedResponse(
            response=make_response(
                render_template("errors/page-not-found.html"), 404
            ),
            timeout=1,
        )
    except Exception:
        return CachedResponse(
            response=make_response(render_template("errors/api.html"), 502),
            timeout=1,
        )
    if (
        "privacy" in page_data["meta"]
        and page_data["meta"]["privacy"] == "password"
    ):
        return redirect(
            url_for("wagtail.preview_protected_page", id=page_data["id"])
        )
    return CachedResponse(
        response=make_response(render_content_page(page_data)),
        timeout=current_app.config["CACHE_DEFAULT_TIMEOUT"],
    )
