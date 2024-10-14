import math

from app.lib import pagination_object
from app.wagtail.api import breadcrumbs, pages_by_type, pages_by_type_paginated
from flask import current_app, render_template, request


def blog_index_page(page_data, year=None, month=None, day=None):
    children_per_page = 24
    children_per_page = 2
    page = (
        int(request.args.get("page"))
        if "page" in request.args and request.args["page"].isnumeric()
        else 1
    )
    try:
        blogs_data = pages_by_type(["blog.BlogPage"], order="title")
        # TODO: Filter children_data by year, month and day
        blog_posts_data = pages_by_type_paginated(
            ["blog.BlogPostPage"],
            page,
            children_per_page + 1 if page == 1 else children_per_page,
            initial_offset=1,
        )
    except ConnectionError:
        current_app.logger.error(
            f"API error getting all blog posts for page {page_data['id']}"
        )
        return render_template("errors/api.html"), 502
    except Exception:
        current_app.logger.error(
            f"Exception getting all blog posts for page {page_data['id']}"
        )
        return render_template("errors/server.html"), 500
    pages = math.ceil(
        blog_posts_data["meta"]["total_count"] / children_per_page
    )
    if page > pages:
        return render_template("errors/page-not-found.html"), 404
    return render_template(
        "blog/index.html",
        breadcrumbs=breadcrumbs(page_data["id"]),
        page_data=page_data,
        blog_posts=blog_posts_data["items"],
        total_blog_posts=blog_posts_data["meta"]["total_count"],
        blogs=blogs_data["items"],
        pagination=pagination_object(page, pages, request.args),
        page=page,
        pages=pages,
        date_filter={"year": year, "month": month, "day": day},
    )
