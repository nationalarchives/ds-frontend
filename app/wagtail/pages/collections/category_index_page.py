from flask import render_template
from tna_utilities.flask import set_cache_control


@set_cache_control("public, no-cache, s-maxage=3600")
def category_index_page(page_data):
    return render_template(
        "explore_the_collection/category_index.html",
        page_data=page_data,
    )
