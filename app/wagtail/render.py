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


def render_content_page(page_data):
    print(page_data)
    page_type = page_data["meta"]["type"]
    if page_type == "home.HomePage":
        return home_page(page_data)
    if page_type == "collections.ExplorerIndexPage":
        return explore_index_page(page_data)
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
        return article_page_focused(page_data)
    if page_type == "collections.HighlightGalleryPage":
        return highlight_gallery_page(page_data)
    if page_type == "authors.AuthorIndexPage":
        return author_index_page(page_data)
    if page_type == "authors.AuthorPage":
        return author_page(page_data)
    current_app.logger.error(f"Template for {page_type} not handled")
    return render_template("errors/page-not-found.html"), 404
