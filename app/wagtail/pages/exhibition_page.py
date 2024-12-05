from app.wagtail.api import breadcrumbs
from flask import render_template


def exhibition_page(page_data):
    return render_template(
        "whats-on/exhibition.html",
        breadcrumbs=breadcrumbs(page_data["id"]),
        page_data=page_data,
    )
