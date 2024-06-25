from app.wagtail.api import breadcrumbs
from flask import render_template


def general_page(page_data):
    return render_template(
        "main/general.html",
        breadcrumbs=breadcrumbs(page_data["id"]),
        page_data=page_data,
    )
