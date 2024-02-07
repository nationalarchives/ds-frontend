from app.wagtail.api import breadcrumbs, page_details
from flask import render_template


def article_page(page_data):
    try:
        similar_items = [
            page_details(page["id"]) for page in page_data["similar_items"]
        ]
        latest_items = [
            page_details(page["id"]) for page in page_data["latest_items"]
        ]
    except ConnectionError:
        return render_template("errors/api.html"), 502
    return render_template(
        "explore/article.html",
        breadcrumbs=breadcrumbs(page_data["id"]),
        page_data=page_data,
        similar_items=similar_items,
        latest_items=latest_items,
    )
