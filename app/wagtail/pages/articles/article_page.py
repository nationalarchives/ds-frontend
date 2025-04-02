from app.wagtail.lib import pages_to_index_grid_items, pick_top_two
from flask import render_template


def article_page(page_data):
    topics = pages_to_index_grid_items(page_data["topics"])
    time_periods = pages_to_index_grid_items(page_data["time_periods"])
    categories = pick_top_two(topics, time_periods)
    return render_template(
        "explore_the_collection/article.html",
        page_data=page_data,
        categories=categories,
    )
