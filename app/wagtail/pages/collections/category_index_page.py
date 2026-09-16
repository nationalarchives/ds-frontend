from flask import render_template
from tna_utilities.flask import cacheable_duration


@cacheable_duration(3600)
def category_index_page(page_data):
    return render_template(
        "explore_the_collection/category_index.html",
        page_data=page_data,
    )
