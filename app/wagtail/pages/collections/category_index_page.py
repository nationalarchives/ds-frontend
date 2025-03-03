from app.wagtail.api import breadcrumbs
from flask import render_template


def category_index_page(page_data):
    return render_template(
        "explore_the_collection/category_index.html",
        breadcrumbs=breadcrumbs(page_data["id"]),
        page_data=page_data,
    )
