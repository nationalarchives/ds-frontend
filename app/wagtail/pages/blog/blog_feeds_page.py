from flask import render_template


def blog_feeds_page(page_data):
    return render_template(
        "feeds/blog.html",
        page_data=page_data,
    )
