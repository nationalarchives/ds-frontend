from flask import render_template

from app.feedback.decorators import process_feedback


@process_feedback
# @cacheable_duration(3600)
def explorer_index_page(page_data, feedback_data):
    return render_template(
        "explore_the_collection/index.html",
        page_data=page_data,
        feedback_data=feedback_data,
    )
