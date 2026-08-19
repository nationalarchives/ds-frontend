import datetime
import math

from flask import current_app, render_template, request
from pydash import objects
from tna_utilities.flask import cacheable_duration
from tna_utilities.url import QueryStringTransformer

from app.error_pages.routes import bad_request_error, page_not_found_error
from app.lib.pagination import pagination
from app.wagtail.api import blog_posts_paginated


@cacheable_duration(3600)
def blog_page(page_data, year=None, month=None, day=None):  # noqa: C901
    children_per_page = 12
    page = 1
    if request.args.get("page"):
        try:
            page = int(request.args.get("page", 1))
        except ValueError:
            current_app.logger.warning(
                f"Invalid page number '{request.args.get('page')}' for page {page_data['id']}"
            )
            return bad_request_error()
    if page < 1:
        current_app.logger.warning(
            f"Page number {page} is less than 1 for page {page_data['id']}"
        )
        return bad_request_error()
    if not year:
        year = request.args.get("year", "")
        if year and not year.isnumeric():
            current_app.logger.warning(
                f"Invalid year '{year}' for page {page_data['id']}"
            )
            return bad_request_error()
        year = int(year) if year else None
    if year is not None:
        if year <= 0:
            current_app.logger.warning(
                f"Year {year} is not a positive integer for page {page_data['id']}"
            )
            return bad_request_error()
        if year > datetime.datetime.now().year:
            current_app.logger.warning(
                f"Year {year} is in the future for page {page_data['id']}"
            )
            return page_not_found_error()
    if not month:
        month = request.args.get("month", "")
        if month and (not month.isnumeric() or int(month) not in range(1, 13)):
            current_app.logger.warning(
                f"Invalid month '{month}' for page {page_data['id']}"
            )
            return bad_request_error()
        month = int(month) if month else None
    try:
        month_name = (
            datetime.date(year or 2000, month, 1).strftime("%B") if month else ""
        )
    except ValueError:
        return bad_request_error()
    blogs_data = page_data.get("top_blogs", [])
    child_blogs = page_data.get("child_blogs", [])
    blog_post_counts_data = page_data.get("blog_posts_count", [])
    authors = page_data.get("blog_posts_authors", [])
    try:
        blog_posts_data = blog_posts_paginated(
            page=page,
            blog_id=page_data["id"],
            year=year,
            month=month,
            limit=children_per_page + 1 if page == 1 else children_per_page,
            initial_offset=0 if page == 1 else 1,
        )
    except Exception:
        current_app.logger.exception(
            f"Failed to get blog posts for page {page_data['id']}"
        )
        blog_posts_data = {}
    total_blog_posts = objects.get(blog_posts_data, "meta.total_count", 0)
    pages = math.ceil(total_blog_posts / children_per_page)
    if total_blog_posts and page > pages:
        return page_not_found_error()
    date_filters = [
        {
            "label": "Any date",
            "href": objects.get(page_data, "meta.url"),
            "title": "Blog posts from any date",
            "selected": not year,
        }
    ]
    qs = QueryStringTransformer(list(request.args.lists()), tolerant=True)
    for year_count in reversed(blog_post_counts_data):
        year_qs = qs.new()
        date_filters.append(
            {
                "label": f"All {year_count['year']} ({year_count['posts']})",
                "href": year_qs.add_parameter("year", year_count["year"])
                .remove_parameter("month")
                .remove_parameter("page")
                .get_query_string(),
                "title": f"Blog posts from {year_count['year']}",
                "selected": qs.is_value_in_parameter("year", year_count["year"])
                and not month,
            }
        )
        if year == year_count["year"]:
            for month_count in reversed(year_count["months"]):
                month_qs = qs.new()
                each_month_name = datetime.date(year, month_count["month"], 1).strftime(
                    "%B"
                )
                date_filters.append(
                    {
                        "label": f"{each_month_name} {year_count['year']} ({month_count['posts']})",
                        "href": month_qs.update_parameter("year", year_count["year"])
                        .update_parameter("month", month_count["month"])
                        .remove_parameter("page")
                        .get_query_string(),
                        "title": f"Blog posts from {each_month_name} {year_count['year']}",
                        "selected": qs.is_value_in_parameter("year", year_count["year"])
                        and qs.is_value_in_parameter("month", month_count["month"]),
                    }
                )
    return render_template(
        "blog/index.html",
        page_data=page_data,
        blog_posts=objects.get(blog_posts_data, "items", []),
        date_filters=date_filters,
        child_blogs=child_blogs,
        total_blog_posts=total_blog_posts,
        blogs=blogs_data,
        authors=authors,
        pagination=pagination(qs, pages, page),
        page=page,
        pages=pages,
        year=year,
        month=month,
        month_name=month_name,
    )
