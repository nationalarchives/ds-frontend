from app.wagtail.api import blogs, breadcrumbs
from flask import current_app, render_template


def blog_post_page(page_data):
    try:
        blogs_data = blogs()
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
        blogs=blogs_data,
        breadcrumbs=breadcrumbs(page_data["id"]),
    )
