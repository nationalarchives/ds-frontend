from flask import render_template


def education_page(page_data):
    return render_template(
        "education/index.html",
        page_data=page_data,
    )
