from flask import render_template


def events_page(page_data):
    return render_template(
        "whats_on/events.html",
        page_data=page_data,
    )
