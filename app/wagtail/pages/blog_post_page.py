from app.wagtail.api import breadcrumbs, pages_by_type
from flask import current_app, render_template


def blog_post_page(page_data):
    try:
        blogs_index_data = pages_by_type(["blog.BlogIndexPage"])
    except ConnectionError:
        current_app.logger.error(
            f"API error getting children for page {page_data['id']}"
        )
        return render_template("errors/api.html"), 502
    except Exception:
        current_app.logger.error(
            f"Exception getting children for page {page_data['id']}"
        )
        return render_template("errors/server.html"), 500
    return render_template(
        "blog/post.html",
        page_data=page_data,
        blogs_index=blogs_index_data["items"],
        breadcrumbs=breadcrumbs(page_data["id"]),
    )
