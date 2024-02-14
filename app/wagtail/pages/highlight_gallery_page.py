from app.catalogue.api import RecordAPI
from app.wagtail.api import breadcrumbs
from flask import render_template

from ..api import image_details


def highlight_gallery_page(page_data):
    for highlight in page_data["page_highlights"]:
        image_id = highlight["image"]
        highlight_image_details = image_details(image_id)
        highlight["image_details"] = highlight_image_details
        if "record" in highlight_image_details:
            record_id = highlight["image_details"]["record"]
            records_api = RecordAPI(record_id)
            record_data = records_api.get_results()
            highlight["record_data"] = record_data
        else:
            highlight["record_data"] = {}
    return render_template(
        "explore/highlight-gallery.html",
        breadcrumbs=breadcrumbs(page_data["id"]),
        page_data=page_data,
    )
