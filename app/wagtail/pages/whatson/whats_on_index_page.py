from app.wagtail.api import page_children
from flask import render_template


def whats_on_index_page(page_data):
    children = page_children(page_data["id"])
    return render_template(
        "whats_on/index.html",
        page_data=page_data,
        children=children.get("items", []),
    )
