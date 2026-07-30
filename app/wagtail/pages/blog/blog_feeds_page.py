from flask import render_template
from tna_utilities.flask import cacheable_duration


@cacheable_duration(14400)
def blog_feeds_page(page_data):
    return render_template(
        "feeds/blog.html",
        page_data=page_data,
    )
