import math

import requests
from flask import current_app, render_template, request

from app.lib import (
    page_children,
    page_children_paginated,
    page_details,
    pagination_list,
)
from app.wagtail import breadcrumbs


def render_explore_page(page_data):
    page_type = page_data["meta"]["type"]
    current_app.logger.debug("Page type %s requested" % page_type)
    if page_type == "articles.ArticleIndexPage":
        return article_index_page(page_data)
    if page_type == "articles.ArticlePage":
        return article_page(page_data)
    if (
        page_type == "collections.TopicExplorerIndexPage"
        or page_type == "collections.TimePeriodExplorerIndexPage"
    ):
        return category_index_page(page_data)
    if (
        page_type == "collections.TopicExplorerPage"
        or page_type == "collections.TimePeriodExplorerPage"
    ):
        return categories_page(page_data)
    if page_type == "articles.RecordArticlePage":
        return record_article_page(page_data)
    if page_type == "articles.FocusedArticlePage":
        return focused_article_page(page_data)
    if page_type == "collections.HighlightGalleryPage":
        return highlight_gallery_page(page_data)
    current_app.logger.error("Template for %s not handled" % page_type)
    return render_template("errors/page-not-found.html"), 404


def category_index_page(page_data):
    try:
        children_data = page_children(page_data["id"])
        all_children = [
            page_details(child["id"]) for child in children_data["items"]
        ]
    except ConnectionError:
        return render_template("errors/api.html"), 502
    children = [
        {
            "id": child["id"],
            "title": child["title"],
            "url": child["meta"]["html_url"],
            "teaser": child["teaser_text"],
            "image": child["teaser_image_jpg"],
        }
        for child in all_children
    ]
    return render_template(
        "explore-category-index.html",
        breadcrumbs=breadcrumbs(page_data["id"]),
        data=page_data,
        children=children,
    )


def categories_page(page_data):
    # TODO

    try:
        children_data = page_children(page_data["id"])
        all_children = [
            page_details(child["id"]) for child in children_data["items"]
        ]
    except ConnectionError:
        return render_template("errors/api.html"), 502
    children = [
        {
            "id": child["id"],
            "title": child["title"],
            "url": child["meta"]["html_url"],
            "teaser": child["teaser_text"],
            "image": child["teaser_image_jpg"],
        }
        for child in all_children
    ]
    return render_template(
        "explore-category.html",
        breadcrumbs=breadcrumbs(page_data["id"]),
        data=page_data,
        children=children,
    )


def article_index_page(page_data):
    children_per_page = 12
    page = int(request.args.get("page")) if "page" in request.args else 1
    try:
        children_data = page_children_paginated(
            page_data["id"], page, children_per_page
        )
    except ConnectionError:
        return render_template("errors/api.html"), 502
    max_pages = math.ceil(
        children_data["meta"]["total_count"] / children_per_page
    )
    if page > max_pages:
        return render_template("errors/page-not-found.html"), 404
    try:
        all_children = [
            page_details(child["id"]) for child in children_data["items"]
        ]
        featured_article = page_details(page_data["featured_article"]["id"])
        all_featured_pages = [
            page_details(featured_page_id)
            for featured_page_id in page_data["featured_pages"][0]["value"][
                "items"
            ]
        ]
    except ConnectionError:
        return render_template("errors/api.html"), 502
    children = [
        {
            "id": child["id"],
            "title": child["title"],
            "url": child["meta"]["html_url"],
            "teaser": child["teaser_text"],
            "supertitle": child["verbose_name_public"]
            if "verbose_name_public" in child
            else "",
            "image": child["teaser_image_jpg"],
        }
        for child in all_children
    ]
    featured_pages = [
        {
            "id": page["id"],
            "title": page["title"],
            "url": page["meta"]["html_url"],
            "teaser": page["teaser_text"],
            "supertitle": page["verbose_name_public"]
            if "verbose_name_public" in page
            else "",
            "image": page["teaser_image_jpg"],
        }
        for page in all_featured_pages
    ]
    return render_template(
        "stories.html",
        breadcrumbs=breadcrumbs(page_data["id"]),
        data=page_data,
        children=children,
        featured_article=featured_article,
        featured_pages=featured_pages,
        pagination_list=pagination_list(page, max_pages, 1, 1),
        page=page,
        max_pages=max_pages,
    )


def article_page(page_data):
    return render_template(
        "article.html",
        breadcrumbs=breadcrumbs(page_data["id"]),
        data=page_data,
    )


def record_article_page(page_data):
    return render_template(
        "record-article.html",
        breadcrumbs=breadcrumbs(page_data["id"]),
        data=page_data,
    )


def focused_article_page(page_data):
    return render_template(
        "focused-article.html",
        breadcrumbs=breadcrumbs(page_data["id"]),
        data=page_data,
    )


def highlight_gallery_page(page_data):
    return render_template(
        "highlight-gallery.html",
        breadcrumbs=breadcrumbs(page_data["id"]),
        data=page_data,
    )
