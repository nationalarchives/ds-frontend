from app.wagtail.api import breadcrumbs, page_children, page_details
from flask import render_template


def author_index_page(page_data):
    try:
        # children_data = page_children(page_data["id"], {"fields": "_,title,teaser_image_jpg,role"})
        children_data = page_children(page_data["id"], {"order": "title"})
        children = [
            page_details(child["id"]) for child in children_data["items"]
        ]
    except ConnectionError:
        return render_template("errors/api.html"), 502
    return render_template(
        "authors/index.html",
        breadcrumbs=breadcrumbs(page_data["id"]),
        children=children,
        page_data=page_data,
    )
