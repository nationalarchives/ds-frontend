from flask import render_template
from tna_utilities.flask import cacheable_duration


@cacheable_duration(3600)
def foi_request_page(page_data):
    return render_template(
        "foi/request.html",
        page_data=page_data,
    )
