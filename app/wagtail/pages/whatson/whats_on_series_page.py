from flask import render_template


def whats_on_series_page(page_data):
    return render_template(
        "whats_on/events.html",
        page_data=page_data,
        events=page_data.get("event_listings", []),
        exhibitions=page_data.get("exhibition_listings", []),
    )
