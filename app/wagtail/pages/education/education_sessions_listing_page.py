from flask import render_template


def education_sessions_listing_page(page_data):
    return render_template(
        "education/listing.html",
        page_data=page_data,
    )
