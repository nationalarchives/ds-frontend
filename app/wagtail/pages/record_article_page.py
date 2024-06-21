from app.catalogue.api import RecordAPI
from app.lib.api import ApiResourceNotFound
from app.wagtail.api import breadcrumbs
from app.wagtail.lib import pages_to_index_grid_items, pick_top_two
from flask import current_app, render_template


def record_article_page(page_data):
    topics = pages_to_index_grid_items(page_data["topics"])
    time_periods = pages_to_index_grid_items(page_data["time_periods"])
    categories = pick_top_two(topics, time_periods)
    page_data["record_data"] = {}
    if "record" in page_data:
        record_id = page_data["record"]
        records_api = RecordAPI(record_id)
        try:
            record_data = records_api.get_results()
            page_data["record_data"] = record_data
        except ApiResourceNotFound:
            current_app.logger.error(
                f"No record details found for record {record_id} in page {page_data['id']}"
            )
        except Exception:
            current_app.logger.error(
                f"Can't get record details for record {record_id} in page {page_data['id']}"
            )
    return render_template(
        "explore-the-collection/record-article.html",
        breadcrumbs=breadcrumbs(page_data["id"]),
        page_data=page_data,
        categories=categories,
    )
