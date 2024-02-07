from app.wagtail.api import breadcrumbs
from flask import render_template


def record_article_page(page_data):
    return render_template(
        "explore/record-article.html",
        breadcrumbs=breadcrumbs(page_data["id"]),
        page_data=page_data,
    )
