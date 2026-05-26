from flask import render_template


def education_session_page(page_data):
    return render_template(
        "education/session.html",
        page_data=page_data,
    )
