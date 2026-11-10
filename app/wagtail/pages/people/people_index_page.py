from flask import render_template


def people_index_page(page_data):
    return render_template(
        "people/index.html",
        page_data=page_data,
    )
