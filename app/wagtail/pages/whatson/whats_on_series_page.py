from flask import render_template
from tna_utilities.flask import set_cache_control


@set_cache_control("public, no-cache, s-maxage=3600")
def whats_on_series_page(page_data):
    return render_template(
        "whats_on/events.html",
        page_data=page_data,
        events=page_data.get("event_listings", []),
        exhibitions=page_data.get("exhibition_listings", []),
    )
