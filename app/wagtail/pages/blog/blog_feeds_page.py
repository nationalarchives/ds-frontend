from flask import render_template
from tna_utilities.flask import cacheable_duration_cloudfront


@cacheable_duration_cloudfront(3600, 14400, 60, 3600)
def blog_feeds_page(page_data):
    return render_template(
        "feeds/blog.html",
        page_data=page_data,
    )
