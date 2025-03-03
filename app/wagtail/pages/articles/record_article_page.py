from app.wagtail.api import breadcrumbs
from app.wagtail.lib import pages_to_index_grid_items, pick_top_two
from flask import render_template


def record_article_page(page_data):
    topics = pages_to_index_grid_items(page_data["topics"])
    time_periods = pages_to_index_grid_items(page_data["time_periods"])
    categories = pick_top_two(topics, time_periods)
    return render_template(
        "explore_the_collection/record_article.html",
        breadcrumbs=breadcrumbs(page_data["id"]),
        page_data=page_data,
        categories=categories,
    )
