from flask import render_template


def education_teaching_resource_page(page_data):
    return render_template(
        "education/teaching_resource.html",
        page_data=page_data,
    )
