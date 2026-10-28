from flask import render_template
from tna_utilities.flask import cacheable_duration_cloudfront


@cacheable_duration_cloudfront(3600, 3600, 60, 3600)
def categories_page(page_data):
    return render_template(
        "explore_the_collection/category.html",
        page_data=page_data,
    )
