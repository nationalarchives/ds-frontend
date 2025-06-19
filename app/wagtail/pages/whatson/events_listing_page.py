from app.wagtail.api import events
from flask import render_template


def events_listing_page(page_data):
    all_events = events()
    return render_template(
        "whats_on/events.html",
        page_data=page_data,
        events=all_events.get("items", []),
    )
