import requests
from app.site import bp
from flask import render_template


def breadcrumbs(page_id):
    ancestors = requests.get(
        "http://host.docker.internal:8000/api/v2/pages/?ancestor_of=%d"
        % page_id
    ).json()
    return [
        {
            "title": "Home"
            if ancestor["meta"]["html_url"] == "http://localhost:65535/"
            else ancestor["title"],
            "url": ancestor["meta"]["html_url"],
        }
        for ancestor in ancestors["items"]
    ]


@bp.route("/")
def hello_world():
    return render_template("welcome.html")


@bp.route("/explore-the-collection/")
def explore():
    explore_data = requests.get(
        "http://host.docker.internal:8000/api/v2/pages/5/"
    ).json()
    large_cards = explore_data["body"][0]["value"]
    large_card_1 = requests.get(
        "http://host.docker.internal:8000/api/v2/pages/%d/"
        % (large_cards["page_1"])
    ).json()
    large_card_2 = requests.get(
        "http://host.docker.internal:8000/api/v2/pages/%d/"
        % (large_cards["page_2"])
    ).json()
    return render_template(
        "explore.html",
        breadcrumbs=breadcrumbs(explore_data["id"]),
        data=explore_data,
        large_cards=[large_card_1, large_card_2],
    )


@bp.route("/explore-the-collection/<path:path>/")
def explore_page(path):
    page_data = requests.get(
        "http://host.docker.internal:8000/api/v2/pages/find/?html_path=/explore-the-collection/%s/"
        % path
    ).json()
    page_type = page_data["meta"]["type"]
    print(page_type)
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
    return render_template("404.html", page_type=page_type)


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
    children_data = requests.get(
        "http://host.docker.internal:8000/api/v2/pages/?child_of=%d"
        % page_data["id"]
    ).json()
    children = [
        {
            "id": child["id"],
            "title": child["title"],
            "url": child["meta"]["html_url"],
            "supertitle": child["verbose_name_public"]
            if "verbose_name_public" in child
            else "",
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
    )


def article_page(page_data):
    return render_template(
        "article.html",
        breadcrumbs=breadcrumbs(page_data["id"]),
        data=page_data,
    )
