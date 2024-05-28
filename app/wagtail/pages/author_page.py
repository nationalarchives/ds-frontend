from app.wagtail.api import breadcrumbs
from flask import render_template


def author_page(page_data):
    return render_template(
        "authors/details.html",
        breadcrumbs=breadcrumbs(page_data["id"]),
        page_data=page_data,
    )
