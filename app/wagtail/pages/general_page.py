from app.wagtail.api import breadcrumbs, page_children
from flask import render_template


def general_page(page_data):
    siblings = []
    if True or page_data["showSiblings"]:
        siblings = page_children(page_data["meta"]["parent"]["id"])
    return render_template(
        "main/general.html",
        breadcrumbs=breadcrumbs(page_data["id"]),
        page_data=page_data,
        siblings=siblings["items"],
    )
