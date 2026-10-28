from flask import render_template


def foi_request_page(page_data):
    return render_template(
        "foi/request.html",
        page_data=page_data,
    )
