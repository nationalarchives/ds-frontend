from app.wagtail.api import breadcrumbs
from flask import render_template


def highlight_gallery_page(page_data):
    return render_template(
        "explore/highlight-gallery.html",
        breadcrumbs=breadcrumbs(page_data["id"]),
        page_data=page_data,
    )
