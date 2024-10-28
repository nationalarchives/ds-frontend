import datetime
import math

from app.lib.pagination import pagination_object
from app.wagtail.api import (
    blog_authors,
    blog_post_counts,
    blog_posts_paginated,
    blogs,
    breadcrumbs,
    page_descendants,
)
from flask import current_app, render_template, request


def blog_page(page_data, year=None, month=None, day=None):
    children_per_page = 12
    page = (
        int(request.args.get("page"))
        if "page" in request.args and request.args["page"].isnumeric()
        else 1
    )
    year = year or (
        int(request.args.get("year"))
        if "year" in request.args and request.args["year"].isnumeric()
        else None
    )
    month = month or (
        int(request.args.get("month"))
        if "month" in request.args and request.args["month"].isnumeric()
        else None
    )
    month_name = (
        datetime.date(year or 2000, month, 1).strftime("%B") if month else ""
    )
    day = day or (
        int(request.args.get("day"))
        if "day" in request.args and request.args["day"].isnumeric()
        else None
    )
    author = request.args.get("author") if "author" in request.args else None
    search = request.args.get("search") if "search" in request.args else None
    search = None  # TODO
    try:
        blogs_data = blogs()
        blog_post_counts_data = blog_post_counts(
            blog_id=page_data["id"],
            author=author,
            # search=search,  # TODO
        )
        blog_posts_data = blog_posts_paginated(
            page=page,
            blog_id=page_data["id"],
            year=year,
            month=month,
            author=author,
            search=search,
            limit=children_per_page + 1 if page == 1 else children_per_page,
            initial_offset=0 if page == 1 else 1,
        )
        categories = page_descendants(
            page_id=page_data["id"], params={"type": "blog.BlogPage"}
        )
        authors = blog_authors(blog_id=page_data["id"])
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
    pages = math.ceil(total_blog_posts / children_per_page)
    if page > pages:
        return render_template("errors/page-not-found.html"), 404
    date_filters = [
        {
            "label": "Any date",
            "href": page_data["meta"]["url"],
            "title": "Blog posts from any date",
            "selected": not year,
        }
    ]
    if year:
        for year_count in reversed(blog_post_counts_data):
            if year_count["year"] == year:
                date_filters.append(
                    {
                        "label": f"All {year_count['year']} ({year_count['posts']})",
                        "href": f"?year={year_count['year']}",
                        "title": f"Blog posts from {year_count['year']}",
                        "selected": not month,
                    }
                )
                for month_count in reversed(year_count["months"]):
                    each_month_name = datetime.date(
                        year, month_count["month"], 1
                    ).strftime("%B")
                    date_filters.append(
                        {
                            "label": f"{each_month_name} {year_count['year']} ({month_count['posts']})",
                            "href": f"?year={year_count['year']}&month={month_count['month']}",
                            "title": f"Blog posts from {each_month_name} {year_count['year']}",
                            "selected": year == year_count["year"]
                            and month == month_count["month"],
                        }
                    )
    else:
        for year_count in reversed(blog_post_counts_data):
            date_filters.append(
                {
                    "label": f"{year_count['year']} ({year_count['posts']})",
                    "href": f"?year={year_count['year']}",
                    "title": f"Blog posts from {year_count['year']}",
                    "selected": False,
                }
            )
    return render_template(
        "blog/index.html",
        breadcrumbs=breadcrumbs(page_data["id"]),
        page_data=page_data,
        blog_posts=blog_posts_data["items"],
        date_filters=date_filters,
        categories=categories["items"],
        total_blog_posts=total_blog_posts,
        blogs=blogs_data,
        authors=authors,
        current_author=next(
            (item for item in authors if item["author"]["slug"] == author), None
        ),
        pagination=pagination_object(page, pages, request.args),
        page=page,
        pages=pages,
        year=year,
        month=month,
        month_name=month_name,
        search=search,
    )
