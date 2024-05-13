from app.wagtail.api import breadcrumbs, page_children, page_details
from flask import render_template


def category_index_page(page_data):
    try:
        children_data = page_children(page_data["id"])
        all_children = [
            page_details(child["id"]) for child in children_data["items"]
        ]
    except ConnectionError:
        return render_template("errors/api.html"), 502
    children = [
        {
            "id": child["id"],
            "title": child["title"],
            "url": child["meta"]["html_url"],
            "teaser": child["teaser_text"],
            "image": child["teaser_image"]["image_jpeg"],
        }
        for child in all_children
    ]
    return render_template(
        "explore/category-index.html",
        breadcrumbs=breadcrumbs(page_data["id"]),
        page_data=page_data,
        children=children,
    )
