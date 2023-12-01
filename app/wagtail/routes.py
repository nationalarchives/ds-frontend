import requests
from flask import request

from app.explore.render import render_explore_page
from app.lib import page_preview
from app.wagtail import bp


@bp.route("/preview/")
def preview_page():
    content_type = request.args.get("content_type")
    token = request.args.get("token")
    page_data = page_preview(content_type, token)
    return render_explore_page(page_data)
