from app.wagtail.api import breadcrumbs
from flask import render_template


def categories_page(page_data):
    return render_template(
        "explore_the_collection/category.html",
        breadcrumbs=breadcrumbs(page_data["id"]),
        page_data=page_data,
    )
