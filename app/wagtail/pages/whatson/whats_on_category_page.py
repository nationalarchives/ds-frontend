from flask import render_template


def whats_on_category_page(page_data):
    return render_template(
        "whats_on/category.html",
        page_data=page_data,
    )
