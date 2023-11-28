import math

import requests
from app.cms import breadcrumbs
from app.lib import pagination_list
from flask import render_template, request


def render_explore_page(page_data):
    page_type = page_data["meta"]["type"]
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
    return render_template("404.html"), 404


def category_index_page(page_data):
    children_data = requests.get(
        "http://host.docker.internal:8000/api/v2/pages/?child_of=%d"
        % page_data["id"]
    ).json()
    children = [
        {
            "id": child["id"],
            "title": child["title"],
            "url": child["meta"]["html_url"],
            "image": requests.get(
                "http://host.docker.internal:8000/api/v2/pages/%d/?fields=_,teaser_image_jpg"
                % child["id"]
            ).json(),
        }
        for child in children_data["items"]
    ]
    return render_template(
        "explore-category-index.html",
        breadcrumbs=breadcrumbs(page_data["id"]),
        data=page_data,
        children=children,
    )


def categories_page(page_data):
    children_data = requests.get(
        "http://host.docker.internal:8000/api/v2/pages/?child_of=%d"
        % page_data["id"]
    ).json()
    children = [
        {
            "id": child["id"],
            "title": child["title"],
            "url": child["meta"]["html_url"],
            "image": requests.get(
                "http://host.docker.internal:8000/api/v2/pages/%d/?fields=_,teaser_image_jpg"
                % child["id"]
            ).json(),
        }
        for child in children_data["items"]
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
    children_data = requests.get(
        "http://host.docker.internal:8000/api/v2/pages/?child_of=%d&offset=%d&limit=%d"
        % (page_data["id"], (page - 1) * children_per_page, children_per_page)
    ).json()
    max_pages = math.ceil(
        children_data["meta"]["total_count"] / children_per_page
    )
    if page > max_pages:
        return render_template("404.html"), 404
    children = [
        {
            "id": child["id"],
            "title": child["title"],
            "url": child["meta"]["html_url"],
            "supertitle": child["verbose_name_public"]
            if "verbose_name_public" in child
            else "",
            "image": requests.get(
                "http://host.docker.internal:8000/api/v2/pages/%d/?fields=_,teaser_image_jpg"
                % child["id"]
            ).json(),
        }
        for child in children_data["items"]
    ]
    featured_article = requests.get(
        "http://host.docker.internal:8000/api/v2/pages/%d/"
        % page_data["featured_article"]["id"]
    ).json()
    featured_pages_data = [
        (
            requests.get(
                "http://host.docker.internal:8000/api/v2/pages/%d/"
                % featured_page_id
            ).json()
        )
        for featured_page_id in page_data["featured_pages"][0]["value"]["items"]
    ]
    featured_pages = [
        {
            "id": page["id"],
            "title": page["title"],
            "url": page["meta"]["html_url"],
            "supertitle": page["verbose_name_public"]
            if "verbose_name_public" in page
            else "",
            "image": requests.get(
                "http://host.docker.internal:8000/api/v2/pages/%d/?fields=_,teaser_image_jpg"
                % page["id"]
            ).json(),
        }
        for page in featured_pages_data
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
