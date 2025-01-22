from app.feeds import bp
from app.lib.api import ApiResourceNotFound
from app.lib.cache import cache, page_cache_key_prefix, rss_feed_cache_key_prefix
from app.wagtail.api import (
    blog_index,
    blog_posts_paginated,
    blogs,
    breadcrumbs,
    global_alerts,
    page_details,
    page_details_by_type,
)
from flask import current_app, make_response, render_template, request, url_for
from flask_caching import CachedResponse


@bp.route("/blog/feeds/")
@cache.cached(key_prefix=page_cache_key_prefix)
def rss_feeds():
    try:
        blog_data = blog_index()
        blogs_data = blogs()
        blogs_data = blogs_data["items"]
    except ConnectionError:
        current_app.logger.error("API error getting all blogs for /feeds/ page")
        return render_template("errors/api.html"), 502
    except Exception:
        current_app.logger.error("Exception getting all blog posts for /feeds/ page")
        return render_template("errors/server.html"), 500
    return render_template(
        "blog/feeds.html",
        global_alert=global_alerts(),
        blog_data=blog_data,
        blogs=blogs_data,
        breadcrumbs=breadcrumbs(blog_data["id"])
        + [{"text": blog_data["title"], "href": blog_data["url"]}],
    )


@bp.route("/blog/feeds/all/")
@cache.cached(timeout=3600, key_prefix=rss_feed_cache_key_prefix)
def rss_all_feed():
    try:
        blog_data = page_details_by_type("blog.BlogIndexPage")
        blog_data = blog_data["items"][0]
        blog_posts = blog_posts_paginated(1, limit=20)
        blog_posts = blog_posts["items"]
    except ConnectionError:
        return CachedResponse(
            response=make_response(render_template("errors/api.html"), 502),
            timeout=1,
        )
    except ApiResourceNotFound:
        return CachedResponse(
            response=make_response(render_template("errors/page_not_found.html"), 404),
            timeout=1,
        )
    except Exception:
        return CachedResponse(
            response=make_response(render_template("errors/api.html"), 502),
            timeout=1,
        )
    xml = render_template(
        (
            "blog/atom_feed.xml"
            if request.args.get("format") == "atom"
            else "blog/rss_feed.xml"
        ),
        url=url_for("feeds.rss_all_feed", _external=True, _scheme="https"),
        blog_data=blog_data,
        blog_posts=blog_posts,
    )
    response = make_response(xml)
    response.headers["Content-Type"] = "text/xml; charset=utf-8"
    return response


@bp.route("/blog/feeds/<int:blog_id>/")
@cache.cached(timeout=3600, key_prefix=rss_feed_cache_key_prefix)
def rss_feed(blog_id):
    try:
        blog_data = page_details(blog_id)
        blog_posts = blog_posts_paginated(1, blog_id=blog_id, limit=20)
        blog_posts = blog_posts["items"]
    except ConnectionError:
        return CachedResponse(
            response=make_response(render_template("errors/api.html"), 502),
            timeout=1,
        )
    except ApiResourceNotFound:
        return CachedResponse(
            response=make_response(render_template("errors/page_not_found.html"), 404),
            timeout=1,
        )
    except Exception:
        return CachedResponse(
            response=make_response(render_template("errors/api.html"), 502),
            timeout=1,
        )
    if blog_data["meta"]["type"] != "blog.BlogPage":
        return CachedResponse(
            response=make_response(render_template("errors/page_not_found.html"), 404),
            timeout=1,
        )
    xml = render_template(
        (
            "blog/atom_feed.xml"
            if request.args.get("format") == "atom"
            else "blog/rss_feed.xml"
        ),
        url=url_for("feeds.rss_feed", blog_id=blog_id, _external=True, _scheme="https"),
        blog_data=blog_data,
        blog_posts=blog_posts,
    )
    response = make_response(xml)
    response.headers["Content-Type"] = "text/xml; charset=utf-8"
    return response
