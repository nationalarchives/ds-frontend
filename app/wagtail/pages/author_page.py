from app.wagtail.api import breadcrumbs, page_details
from flask import render_template


def author_page(page_data):
    authored_focused_articles = []
    try:
        authored_focused_articles = [
            page_details(child["id"])
            for child in page_data["authored_focused_articles"]
        ]
    except ConnectionError:
        return render_template("errors/api.html"), 502
    return render_template(
        "authors/details.html",
        breadcrumbs=breadcrumbs(page_data["id"]),
        page_data=page_data,
        authored_focused_articles=authored_focused_articles,
    )
