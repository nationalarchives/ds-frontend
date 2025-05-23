from flask import render_template


def whats_on_series_page(page_data):
    return render_template(
        "whats_on/series.html",
        page_data=page_data,
    )
