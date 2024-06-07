from app.lib import cache, cache_key_prefix
from app.lib.api import ApiResourceNotFound, ApiResourceProtected
from app.wagtail import bp
from app.wagtail.render import render_content_page
from flask import current_app, make_response, render_template, request
from flask_caching import CachedResponse

from .api import (
    page_details_by_uri,
    page_preview,
    password_protected_page_details_by_uri,
)


@bp.route("/preview/")
def preview_page():
    content_type = request.args.get("content_type")
    token = request.args.get("token")
    page_data = page_preview(content_type, token)
    return render_content_page(page_data | {"page_preview": True})


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


@bp.route("/<path:path>/", methods=["GET"])
@cache.cached(key_prefix=cache_key_prefix)
def explore_page(path):
    try:
        page_data = page_details_by_uri(path)
    except ConnectionError:
        return CachedResponse(
            response=make_response(render_template("errors/api.html"), 502),
            timeout=1,
        )
    except ApiResourceNotFound:
        try:
            current_app.logger.info("Trying password protected page")
            password_protected_page_details_by_uri(path)
        except ApiResourceProtected:
            return CachedResponse(
                response=make_response(
                    render_template(
                        "errors/password-protected.html", page_data={}
                    )
                ),
                timeout=1,
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


@bp.route("/<path:path>/", methods=["POST"])
@cache.cached(key_prefix=cache_key_prefix)
def explore_page_password_protected(path):
    try:
        page_data = password_protected_page_details_by_uri(
            path, {"password": request.form["password"]}
        )
    except ApiResourceProtected:
        page_data = {}
        if "password" in request.form:
            if request.form["password"] == "":
                page_data["error"] = "Enter a password"
            else:
                page_data["error"] = "Incorrect password"
        return CachedResponse(
            response=make_response(
                render_template(
                    "errors/password-protected.html", page_data=page_data
                )
            ),
            timeout=1,
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
    return CachedResponse(
        response=make_response(render_content_page(page_data)),
        timeout=current_app.config["CACHE_DEFAULT_TIMEOUT"],
    )
