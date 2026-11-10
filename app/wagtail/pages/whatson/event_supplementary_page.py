from flask import render_template


def event_supplementary_page(page_data):
    return render_template("main/general.html", page_data=page_data)
