from app.feeds import bp
from app.lib.api import ResourceNotFound
from app.wagtail.api import (
    blog_posts_paginated,
    page_details,
    page_details_by_type,
)
from flask import current_app, make_response, render_template, request, url_for
from pydash import objects


@bp.route("/blogs.xml")
def rss_all_feed():
    items = current_app.config["ITEMS_PER_BLOG_FEED"]
    try:
        blog_data = page_details_by_type("blog.BlogIndexPage")
        blog_posts = blog_posts_paginated(page=1, limit=items)
    except Exception as e:
        current_app.logger.error(f"Failed to render blog feeds list: {e}")
        return render_template("errors/api.html"), 502
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
def rss_feed(blog_id):
    items = current_app.config["ITEMS_PER_BLOG_FEED"]
    try:
        blog_data = page_details(blog_id)
        blog_posts = blog_posts_paginated(1, blog_id=blog_id, limit=items)
    except ResourceNotFound:
        return render_template("errors/page_not_found.html"), 404
    except Exception as e:
        current_app.logger.error(f"Failed to get blog data for page {blog_id}: {e}")
        return render_template("errors/api.html"), 502
    if objects.get(blog_data, "meta.type") != "blog.BlogPage":
        return render_template("errors/page_not_found.html"), 404
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
