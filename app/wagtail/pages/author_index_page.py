from app.wagtail.api import breadcrumbs, page_children
from flask import render_template


def author_index_page(page_data):
    try:
        children = page_children(
            page_data["id"],
            {
                "type": "authors.AuthorPage",
                "fields": "_,title,teaser_image,role,html_url",
                "order": "title",
            },
        )
    except ConnectionError:
        return render_template("errors/api.html"), 502
    return render_template(
        "authors/index.html",
        breadcrumbs=breadcrumbs(page_data["id"]),
        children=children["items"],
        page_data=page_data,
    )
