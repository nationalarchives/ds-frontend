from flask import render_template
from tna_utilities.flask import set_cache_control


@set_cache_control("public, no-cache, s-maxage=14400")
def blog_feeds_page(page_data):
    return render_template(
        "feeds/blog.html",
        page_data=page_data,
    )
