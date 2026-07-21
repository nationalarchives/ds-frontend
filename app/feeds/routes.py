from flask import current_app, make_response, render_template, request, url_for
from pydash import objects
from tna_utilities.api import ResourceNotFoundError
from tna_utilities.flask import cacheable_duration

from app.error_pages.routes import bad_gateway_error, page_not_found_error
from app.feeds import bp
from app.wagtail.api import (
    blog_posts_paginated,
    page_details,
    page_details_by_type,
)


@bp.route("/blogs.xml")
@cacheable_duration(14400)
def rss_all_feed():
    items = current_app.config["ITEMS_PER_BLOG_FEED"]
    try:
        blog_data = page_details_by_type("blog.BlogIndexPage")
        blog_posts = blog_posts_paginated(page=1, limit=items)
    except Exception:
        current_app.logger.exception("Failed to render blog feeds list")
        return bad_gateway_error()
    xml = render_template(
        (
            "feeds/blog_atom_feed.xml"
            if request.args.get("format") == "atom"
            else "feeds/blog_rss_feed.xml"
        ),
        url=url_for("feeds.rss_all_feed", _external=True, _scheme="https"),
        blog_data=objects.get(blog_data, "items.0", {}) | {"meta": {"slug": "all"}},
        blog_posts=objects.get(blog_posts, "items", []),
    )
    response = make_response(xml)
    response.headers["Content-Type"] = "text/xml; charset=utf-8"
    return response


@bp.route("/blogs/<int:blog_id>.xml")
@cacheable_duration(14400)
def rss_feed(blog_id):
    items = current_app.config["ITEMS_PER_BLOG_FEED"]
    try:
        blog_data = page_details(blog_id)
        blog_posts = blog_posts_paginated(1, blog_id=blog_id, limit=items)
    except ResourceNotFoundError:
        return page_not_found_error()
    except Exception:
        current_app.logger.exception(f"Failed to get blog data for page {blog_id}")
        return bad_gateway_error()
    if objects.get(blog_data, "meta.type") != "blog.BlogPage":
        return page_not_found_error()
    xml = render_template(
        (
            "feeds/blog_atom_feed.xml"
            if request.args.get("format") == "atom"
            else "feeds/blog_rss_feed.xml"
        ),
        url=url_for("feeds.rss_feed", blog_id=blog_id, _external=True, _scheme="https"),
        blog_data=blog_data,
        blog_posts=objects.get(blog_posts, "items", []),
    )
    response = make_response(xml)
    response.headers["Content-Type"] = "text/xml; charset=utf-8"
    return response
