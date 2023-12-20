from app.lib import cache
from app.wagtail import bp
from app.wagtail.render import render_content_page
from flask import render_template, request, current_app

from .api import page_details_by_uri, page_preview


def make_cache_key_prefix():
    """Make a key that includes GET parameters."""
    return request.full_path


@bp.route("/preview/")
def preview_page(key_prefix=make_cache_key_prefix):
    content_type = request.args.get("content_type")
    token = request.args.get("token")
    page_data = page_preview(content_type, token)
    return render_content_page(page_data)


@bp.route("/<path:path>/")
@cache.cached(key_prefix=make_cache_key_prefix)
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
