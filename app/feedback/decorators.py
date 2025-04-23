import functools

from app.feedback.api import (
    page_feedback_form,
    page_feedback_form_by_id,
    submit_additional_feedback,
    submit_first_feedback,
)
from app.lib.template_filters import qs_toggler
from flask import redirect, request


def process_feedback(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        feedback_form_id = request.args.get("feedback_form_id")
        feedback_form = (
            page_feedback_form_by_id(feedback_form_id)
            if feedback_form_id
            else page_feedback_form(request.path)
        )
        response_id = request.args.get("response_id")
        feedback_prompt_id = request.args.get("feedback_prompt_id")
        feedback_value = ""
        for prompt in feedback_form["prompts"]:
            if prompt["id"] == feedback_prompt_id:
                feedback_value = request.args.get(feedback_prompt_id)
                break
        if feedback_prompt_id and feedback_value:
            if response_id:
                try:
                    submit_additional_feedback(
                        response_id,
                        feedback_prompt_id,
                        feedback_value,
                    )
                except Exception:
                    pass
            else:
                try:
                    respone = submit_first_feedback(
                        request.path,
                        feedback_form_id,
                        feedback_prompt_id,
                        feedback_value,
                        metadata={
                            "user_agent": request.headers.get("User-Agent"),
                        },
                    )
                    response_id = respone["id"]
                    new_params = qs_toggler(
                        request.args.to_dict(), "response_id", response_id
                    )
                    return redirect(f"{request.path}?{new_params}", 307)
                except Exception:
                    pass
        feedback_data = {
            "feedback_form": feedback_form,
            "response_id": response_id,
        }
        value = func(*args, **kwargs, feedback_data=feedback_data)
        return value

    return wrapper
