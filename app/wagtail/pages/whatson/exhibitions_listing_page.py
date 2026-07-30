from flask import render_template
from tna_utilities.flask import cacheable_duration


@cacheable_duration(3600)
def exhibitions_listing_page(page_data):
    return render_template(
        "whats_on/exhibitions.html",
        page_data=page_data,
    )
