from app.feedback.decorators import process_feedback
from flask import render_template


@process_feedback
def exhibition_page(page_data, feedback_data):
    return render_template(
        "whats_on/exhibition.html",
        page_data=page_data,
        feedback_data=feedback_data,
    )
