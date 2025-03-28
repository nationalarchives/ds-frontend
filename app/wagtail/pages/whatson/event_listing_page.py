from flask import render_template


def event_listing_page(page_data):
    return render_template(
        "whats_on/event_listing_page.html",
        page_data=page_data,
    )
