from app.wagtail.api import breadcrumbs
from flask import render_template


def whats_on_page(page_data):
    return render_template(
        "whats_on/index.html",
        breadcrumbs=breadcrumbs(page_data["id"]),
        page_data=page_data,
    )
