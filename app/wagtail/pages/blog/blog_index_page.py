import datetime
import math
from tna_utilities.urls import QueryStringTransformer

from app.lib.pagination import pagination_object
from app.lib.query import qs_active, qs_toggler
from app.wagtail.api import (
    blog_authors,
    blog_post_counts,
    blog_posts_paginated,
    top_blogs,
)
from flask import current_app, render_template, request
from pydash import objects


def blog_index_page(page_data, year=None, month=None, day=None):
    children_per_page = 12
    page = (
        int(request.args.get("page"))
        if request.args.get("page") and request.args.get("page").isnumeric()
        else 1
    )
    year = year or (
        int(request.args.get("year"))
        if request.args.get("year") and request.args.get("year").isnumeric()
        else (
            datetime.datetime.now().year
            if request.args.get("month") or request.args.get("day")
            else None
        )
    )
    month = month or (
        int(request.args.get("month"))
        if request.args.get("month") and request.args.get("month").isnumeric()
        else datetime.datetime.now().month if request.args.get("day") else None
    )
    month_name = datetime.date(year or 2000, month, 1).strftime("%B") if month else ""
    day = day or (
        int(request.args.get("day"))
        if request.args.get("day") and request.args.get("day").isnumeric()
        else None
    )
    blogs_data = top_blogs()
    blog_post_counts_data = blog_post_counts()
    authors = blog_authors()
    try:
        blog_posts_data = blog_posts_paginated(
            page=page,
            year=year,
            month=month,
            limit=children_per_page + 1 if page == 1 else children_per_page,
            initial_offset=0 if page == 1 else 1,
        )
    except Exception as e:
        current_app.logger.error(
            f"Failed to get blog posts for page {page_data["id"]}: {e}"
        )
        blog_posts_data = {}
    total_blog_posts = objects.get(blog_posts_data, "meta.total_count", 0)
    pages = math.ceil(total_blog_posts / children_per_page)
    if total_blog_posts and page > pages:
        return render_template("errors/page_not_found.html"), 404



    # existing_qs_as_dict = request.args.to_dict()
    # normalised_args = list(request.args.lists())
    # qs = QueryStringTransformer(normalised_args)




    date_filters = [
        {
            "label": "Any date",
            "href": objects.get(page_data, "meta.url"),
            "title": "Blog posts from any date",
            "selected": not year,
        }
    ]
    for year_count in reversed(blog_post_counts_data):
        date_filters.append(
            {
                "label": f"All {year_count['year']} ({year_count['posts']})",
                "href": "?"
                + (
                    qs_toggler(existing_qs_as_dict, "month", month)
                    if year == year_count["year"] and month
                    else f"year={year_count['year']}"
                ),
                "title": f"Blog posts from {year_count['year']}",
                "selected": qs_active(existing_qs_as_dict, "year", year_count["year"])
                and not month,
            }
        )
        if year == year_count["year"]:
            for month_count in reversed(year_count["months"]):
                each_month_name = datetime.date(year, month_count["month"], 1).strftime(
                    "%B"
                )
                date_filters.append(
                    {
                        "label": f"{each_month_name} {year_count['year']} ({month_count['posts']})",
                        "href": "?"
                        + (
                            f"year={year_count['year']}&month={month_count['month']}"
                            if month == month_count["month"]
                            else qs_toggler(
                                existing_qs_as_dict,
                                "month",
                                month_count["month"],
                            )
                        ),
                        "title": f"Blog posts from {each_month_name} {year_count['year']}",
                        "selected": qs_active(
                            existing_qs_as_dict, "year", year_count["year"]
                        )
                        and qs_active(
                            existing_qs_as_dict, "month", month_count["month"]
                        ),
                    }
                )
    return render_template(
        "blog/index.html",
        page_data=page_data,
        blog_posts=objects.get(blog_posts_data, "items", []),
        date_filters=date_filters,
        total_blog_posts=total_blog_posts,
        blogs=blogs_data,
        authors=authors,
        pagination=pagination_object(page, pages, request.args),
        page=page,
        pages=pages,
        year=year,
        month=month,
        month_name=month_name,
    )
