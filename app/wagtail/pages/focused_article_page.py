from app.wagtail.api import breadcrumbs, page_details
from flask import render_template


def focused_article_page(page_data):
    try:
        authors = (
            [page_details(author["author"]) for author in page_data["authors"]]
            if page_data["authors"]
            else []
        )
    except ConnectionError:
        return render_template("errors/api.html"), 502
    return render_template(
        "explore/focused-article.html",
        breadcrumbs=breadcrumbs(page_data["id"]),
        page_data=page_data,
        authors=authors,
    )
