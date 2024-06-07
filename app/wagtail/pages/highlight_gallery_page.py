from app.catalogue.api import RecordAPI
from app.wagtail.api import breadcrumbs
from app.wagtail.lib import pages_to_index_grid_items, pick_top_two
from flask import render_template


def highlight_gallery_page(page_data):
    topics = pages_to_index_grid_items(page_data["topics"], "Topic")
    time_periods = pages_to_index_grid_items(
        page_data["time_periods"], "Time period"
    )
    categories = pick_top_two(topics, time_periods)
    for highlight in page_data["highlights"]:
        highlight["record_data"] = {}
        if "record" in highlight["image"]:
            record_id = highlight["image"]["record"]
            records_api = RecordAPI(record_id)
            record_data = records_api.get_results()
            highlight["record_data"] = record_data
    return render_template(
        "explore-the-collection/highlight-gallery.html",
        breadcrumbs=breadcrumbs(page_data["id"]),
        page_data=page_data,
        categories=categories,
    )
