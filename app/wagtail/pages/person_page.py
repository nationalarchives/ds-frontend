import math

from app.lib.pagination import pagination_object
from app.wagtail.api import authors_paginated, breadcrumbs
from flask import current_app, render_template, request
from pydash import objects


def person_page(page_data):
    articles_preview_list = 2
    articles_per_page = 1
    page = (
        int(request.args.get("page"))
        if request.args.get("page") and request.args.get("page").isnumeric()
        else 0
    )
    try:
        articles = authors_paginated(page_data["id"], page or 1)
    except ConnectionError:
        current_app.logger.error(
            f"API error getting author articles for page {page_data['id']}"
        )
        return render_template("errors/api.html"), 502
    except Exception:
        current_app.logger.error(
            f"Exception getting author articles for page {page_data['id']}"
        )
        return render_template("errors/server.html"), 500
    total_article_count = objects.get(articles, "meta.total_count", 0)
    print(total_article_count)
    articles = objects.get(articles, "items", [])
    pages = math.ceil(total_article_count / articles_per_page)
    if page > pages:
        return render_template("errors/page-not-found.html"), 404
    return render_template(
        "people/person.html",
        breadcrumbs=breadcrumbs(page_data["id"]),
        page_data=page_data,
        pagination=pagination_object(page, pages, request.args),
        page=page,
        pages=pages,
        articles=articles if page else articles[0:articles_preview_list],
        more_articles=total_article_count > articles_preview_list,
    )
