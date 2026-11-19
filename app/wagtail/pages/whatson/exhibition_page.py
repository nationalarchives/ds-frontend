from flask import render_template


def exhibition_page(page_data):
    return render_template(
        "whats_on/exhibition.html",
        page_data=page_data,
    )
