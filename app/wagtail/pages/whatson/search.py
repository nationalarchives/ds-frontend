from flask import render_template


def whats_on_search_page(page_data):
    return render_template(
        "whats_on/search.html",
        page_data=page_data,
    )
