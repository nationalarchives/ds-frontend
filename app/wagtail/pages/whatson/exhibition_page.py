from app.feedback.decorators import process_feedback
from flask import render_template
from tna_utilities.flask import cacheable_duration


@process_feedback
def exhibition_page_2(page_data, feedback_data):
    return "FOO"

@cacheable_duration(3600)
def exhibition_page(page_data):
    return render_template(
        "whats_on/exhibition.html",
        page_data=page_data,
    )
