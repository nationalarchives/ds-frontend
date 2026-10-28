from flask import render_template
from tna_utilities.flask import cacheable_duration_cloudfront


@cacheable_duration_cloudfront(3600, 3600, 60, 3600)
def whats_on_category_page(page_data):
    return render_template(
        "whats_on/events.html",
        page_data=page_data,
        events=page_data.get("event_listings", []),
    )
