from flask import render_template


def home_page(page_data):
    return render_template(
        "main/home.html",
        page_data=page_data,
    )
