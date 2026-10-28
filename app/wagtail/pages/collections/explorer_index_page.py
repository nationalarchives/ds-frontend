from flask import render_template


def explorer_index_page(page_data):
    return render_template("explore_the_collection/index.html", page_data=page_data)
