from flask import render_template
from tna_utilities.flask import cacheable_duration_cloudfront


@cacheable_duration_cloudfront(3600, 3600, 60, 3600)
def cookie_details_page(page_data):
    page_data["page_sidebar"] = "contents"
    return render_template(
        "main/general.html",
        page_data=page_data,
    )
