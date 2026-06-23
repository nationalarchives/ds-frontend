from flask import render_template
from tna_utilities.flask import cacheable_duration


@cacheable_duration(3600)
def event_supplementary_page(page_data):
    return render_template("whats_on/event_supplementary.html", page_data=page_data)
