from flask import render_template


def exhibitions_listing_page(page_data):
    return render_template(
        "whats_on/exhibitions.html",
        page_data=page_data,
    )
