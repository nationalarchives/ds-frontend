from flask import current_app, render_template

from .pages import (
    article_index_page,
    article_page,
    article_page_focused,
    categories_page,
    category_index_page,
    explore_index_page,
    general_page,
    highlight_gallery_page,
    home_page,
    hub_page,
    people_index_page,
    person_page,
    record_article_page,
)

page_type_templates = {
    # General
    "home.HomePage": home_page,
    "generic_pages.GeneralPage": general_page,
    "generic_pages.HubPage": hub_page,
    # Explore the collection
    "collections.ExplorerIndexPage": explore_index_page,
    "collections.HighlightGalleryPage": highlight_gallery_page,
    "collections.TimePeriodExplorerIndexPage": category_index_page,
    "collections.TimePeriodExplorerPage": categories_page,
    "collections.TopicExplorerIndexPage": category_index_page,
    "collections.TopicExplorerPage": categories_page,
    # Articles
    "articles.ArticleIndexPage": article_index_page,
    "articles.ArticlePage": article_page,
    "articles.FocusedArticlePage": article_page_focused,
    "articles.RecordArticlePage": record_article_page,
    # People
    "people.PeopleIndexPage": people_index_page,
    "people.PersonPage": person_page,
}


def render_content_page(page_data):
    if "meta" in page_data and "type" in page_data["meta"]:
        page_type = page_data["meta"]["type"]
        if page_type in page_type_templates:
            return page_type_templates[page_type](page_data)
        current_app.logger.error(f"Template for {page_type} not handled")
        return render_template("errors/page-not-found.html"), 404
    current_app.logger.error("Page meta information not included")
    return render_template("errors/api.html"), 502
