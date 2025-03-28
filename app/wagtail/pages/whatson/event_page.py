from flask import render_template


def event_page(page_data):
    return render_template(
        "whats_on/event.html",
        page_data=page_data,
    )
