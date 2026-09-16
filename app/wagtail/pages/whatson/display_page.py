from flask import render_template
from tna_utilities.flask import cacheable_duration


@cacheable_duration(3600)
def display_page(page_data):
    return render_template(
        "whats_on/display.html",
        page_data=page_data,
    )
