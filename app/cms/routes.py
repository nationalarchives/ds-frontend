import requests
from app.explore import bp
from app.explore.render import render_explore_page
from flask import request


@bp.route("/preview/")
def preview_page():
    content_type = request.args.get("content_type")
    token = request.args.get("token")
    page_data = requests.get(
        "http://host.docker.internal:8000/api/v2/page_preview/1/?content_type=%s&token=%s&format=json"
        % (content_type, token)
    ).json()
    return render_explore_page(page_data)
