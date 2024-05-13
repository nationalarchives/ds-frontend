from app.catalogue.api import RecordAPI
from app.wagtail.api import breadcrumbs
from app.wagtail.lib import pages_to_index_grid_items, pick_top_two
from flask import render_template


def record_article_page(page_data):
    topics = pages_to_index_grid_items(page_data["topics"], "Topic")
    time_periods = pages_to_index_grid_items(
        page_data["time_periods"], "Time period"
    )
    highlights = pick_top_two(topics, time_periods)
    page_data["record_data"] = {}
    if "record" in page_data:
        record_id = page_data["record"]
        records_api = RecordAPI(record_id)
        record_data = records_api.get_results()
        page_data["record_data"] = record_data
    return render_template(
        "explore/record-article.html",
        breadcrumbs=breadcrumbs(page_data["id"]),
        page_data=page_data,
        highlights=highlights,
    )
