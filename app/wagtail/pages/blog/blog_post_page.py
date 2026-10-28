from flask import render_template
from tna_utilities.flask import set_cache_control


@set_cache_control("public, no-cache, s-maxage=3600")
def blog_post_page(page_data):
    return render_template(
        "blog/post.html",
        page_data=page_data,
    )
