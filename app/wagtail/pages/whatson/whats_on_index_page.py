from flask import render_template


def whats_on_index_page(page_data):
    return render_template(
        "whats_on/index.html",
        page_data=page_data,
    )
