from app.lib import cache, cache_key_prefix
from app.wagtail import bp
from app.wagtail.render import render_content_page
from flask import current_app, render_template, request

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
        return render_template("errors/api.html"), 502
    except Exception:
        current_app.logger.error("An exception occurred on home page")
        return render_template("errors/page-not-found.html"), 404
    return render_content_page(page_data)


@bp.route("/<path:path>/")
@cache.cached(key_prefix=cache_key_prefix)
def explore_page(path):
    try:
        page_data = page_details_by_uri(path)
    except ConnectionError:
        current_app.logger.error(f"ConnectionError for {path}")
        return render_template("errors/api.html"), 502
    except Exception:
        current_app.logger.error(f"An exception occurred on {path}")
        return render_template("errors/page-not-found.html"), 404
    return render_content_page(page_data)
