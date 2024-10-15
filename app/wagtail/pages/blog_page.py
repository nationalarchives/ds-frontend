import math

from app.lib import pagination_object
from app.wagtail.api import (
    breadcrumbs,
    page_descendants,
    page_descendants_paginated,
    pages_by_type,
)
from flask import current_app, render_template, request


def blog_page(page_data, year=None, month=None, day=None):
    children_per_page = 24
    page = (
        int(request.args.get("page"))
        if "page" in request.args and request.args["page"].isnumeric()
        else 1
    )
    try:
        blogs_index_data = pages_by_type(["blog.BlogIndexPage"])
        blogs_data = pages_by_type(["blog.BlogPage"], order="title")
        # TODO: Filter children_data by year, month and day
        child_blogs_data = page_descendants(
            page_id=page_data["id"], params={"type": "blog.BlogPage"}
        )
        blog_posts_data = page_descendants_paginated(
            page_id=page_data["id"],
            page=page,
            limit=children_per_page + 1 if page == 1 else children_per_page,
            initial_offset=0 if page == 1 else 1,
            params={"type": "blog.BlogPostPage"},
        )
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
    total_blog_posts = blog_posts_data["meta"]["total_count"]
    categories = [child_blog for child_blog in child_blogs_data["items"]]
    category_ids = [blog["id"] for blog in categories]
    blogs = [
        blog for blog in blogs_data["items"] if blog["id"] not in category_ids
    ]
    # blogs = []  # TODO: Do we need other blogs?
    pages = math.ceil(total_blog_posts / children_per_page)
    if page > pages:
        return render_template("errors/page-not-found.html"), 404
    return render_template(
        "blog/index.html",
        breadcrumbs=breadcrumbs(page_data["id"]),
        page_data=page_data,
        blogs_index=blogs_index_data["items"],
        blogs=blogs,
        categories=categories,
        blog_posts=blog_posts_data["items"],
        total_blog_posts=total_blog_posts,
        pagination=pagination_object(page, pages, request.args),
        page=page,
        pages=pages,
        date_filter={"year": year, "month": month, "day": day},
    )
