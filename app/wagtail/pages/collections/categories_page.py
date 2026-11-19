from flask import render_template


def categories_page(page_data):
    return render_template(
        "explore_the_collection/category.html",
        page_data=page_data,
    )
