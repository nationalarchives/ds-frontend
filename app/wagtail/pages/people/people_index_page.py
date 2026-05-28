from flask import render_template
from tna_utilities.flask import cacheable_duration


@cacheable_duration(3600)
def people_index_page(page_data):
    return render_template(
        "people/index.html",
        page_data=page_data,
    )
