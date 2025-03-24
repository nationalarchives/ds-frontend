from app.wagtail.api import breadcrumbs
from flask import render_template


def event_page(page_data):
    return render_template(
        "whats_on/event.html",
        breadcrumbs=breadcrumbs(page_data["id"]),
        page_data=page_data,
    )
