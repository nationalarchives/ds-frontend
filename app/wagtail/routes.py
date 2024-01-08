from app.lib import cache, cache_key_prefix
from app.wagtail import bp
from app.wagtail.render import render_content_page
from config import cache_config
from flask import current_app, make_response, render_template, request
from flask_caching import CachedResponse

from .api import page_details_by_uri, page_preview


@bp.route("/preview/")
def preview_page(key_prefix=cache_key_prefix):
    content_type = request.args.get("content_type")
    token = request.args.get("token")
    page_data = page_preview(content_type, token)
    return render_content_page(page_data)


@bp.route("/")
@cache.cached(key_prefix=cache_key_prefix)
def index():
    try:
        page_data = page_details_by_uri("/")
    except ConnectionError:
        current_app.logger.error("ConnectionError for home page")
        return CachedResponse(
            response=make_response(render_template("errors/api.html"), 502),
            timeout=1,
        )
    except Exception:
        current_app.logger.error("An exception occurred on home page")
        return CachedResponse(
            response=make_response(
                render_template("errors/page-not-found.html"), 404
            ),
            timeout=1,
        )
    return CachedResponse(
        response=make_response(render_content_page(page_data)),
        timeout=cache_config["CACHE_DEFAULT_TIMEOUT"],
    )


@bp.route("/<path:path>/")
@cache.cached(key_prefix=cache_key_prefix)
def explore_page(path):
    try:
        page_data = page_details_by_uri(path)
    except ConnectionError:
        current_app.logger.error(f"ConnectionError for {path}")
        return CachedResponse(
            response=make_response(render_template("errors/api.html"), 502),
            timeout=1,
        )
    except Exception:
        current_app.logger.error(f"An exception occurred on {path}")
        return CachedResponse(
            response=make_response(
                render_template("errors/page-not-found.html"), 404
            ),
            timeout=1,
        )
    return CachedResponse(
        response=make_response(render_content_page(page_data)),
        timeout=cache_config["CACHE_DEFAULT_TIMEOUT"],
    )
