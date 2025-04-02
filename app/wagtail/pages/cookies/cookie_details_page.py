from flask import render_template


def cookie_details_page(page_data):
    page_data["page_sidebar"] = "contents"
    return render_template(
        "main/general.html",
        page_data=page_data,
    )
