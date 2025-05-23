from flask import render_template


def display_page(page_data):
    return render_template(
        "whats_on/display.html",
        page_data=page_data,
    )
