from app.wagtail.api import breadcrumbs
from flask import render_template


def blog_post_page(page_data):
    return render_template(
        "blog/post.html",
        page_data=page_data,
        breadcrumbs=breadcrumbs(page_data["id"]),
    )
