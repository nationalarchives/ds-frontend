from flask import render_template
from tna_utilities.flask import cacheable_duration


@cacheable_duration(3600)
def events_listing_page(page_data):
    return render_template(
        "whats_on/events.html",
        page_data=page_data,
        events=page_data.get("event_listings", []),
    )
