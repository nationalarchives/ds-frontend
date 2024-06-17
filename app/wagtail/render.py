from flask import current_app, render_template

from .pages import (
    article_index_page,
    article_page,
    article_page_focused,
    author_index_page,
    author_page,
    categories_page,
    category_index_page,
    explore_index_page,
    highlight_gallery_page,
    home_page,
    record_article_page,
)

page_type_templates = {
    "home.HomePage": home_page,
    "collections.ExplorerIndexPage": explore_index_page,
    "collections.TopicExplorerIndexPage": category_index_page,
    "collections.TimePeriodExplorerIndexPage": category_index_page,
    "collections.TopicExplorerPage": categories_page,
    "collections.TimePeriodExplorerPage": categories_page,
    "collections.HighlightGalleryPage": highlight_gallery_page,
    "articles.ArticleIndexPage": article_index_page,
    "articles.ArticlePage": article_page,
    "articles.RecordArticlePage": record_article_page,
    "articles.FocusedArticlePage": article_page_focused,
    "authors.AuthorIndexPage": author_index_page,
    "authors.AuthorPage": author_page,
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
