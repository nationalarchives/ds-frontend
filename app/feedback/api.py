from flask import current_app
from tna_utilities.api import SimpleJsonApiClient


def feedback_api_client():
    api_url = current_app.config.get("FEEDBACK_API_URL")
    if not api_url:
        current_app.logger.error("FEEDBACK_API_URL not set")
        raise ValueError("FEEDBACK_API_URL not set")
    api_key = current_app.config.get("FEEDBACK_API_KEY")
    if not api_key:
        current_app.logger.error("FEEDBACK_API_KEY not set")
        raise ValueError("FEEDBACK_API_KEY not set")
    client = SimpleJsonApiClient(
        api_url, default_headers={"Authorization": f"Token {api_key}"}
    )
    return client


def page_feedback_form(path):
    project_id = current_app.config.get("FEEDBACK_PROJECT_ID")
    if not project_id:
        current_app.logger.error("FEEDBACK_PROJECT_ID not set")
        raise ValueError("FEEDBACK_PROJECT_ID not set")
    uri = f"/core/projects/{project_id}/feedback-forms/path{path}"
    print(f"Fetching feedback form for path: {path}")
    print(uri)
    return feedback_api_client().get(uri)


def page_feedback_form_by_id(form_id):
    project_id = current_app.config.get("FEEDBACK_PROJECT_ID")
    if not project_id:
        current_app.logger.error("FEEDBACK_PROJECT_ID not set")
        raise ValueError("FEEDBACK_PROJECT_ID not set")
    uri = f"/core/projects/{project_id}/feedback-forms/{form_id}/"
    return feedback_api_client().get(uri)


def submit_first_feedback(
    path, feedback_form_id, first_prompt_id, first_prompt_value, metadata=None
):
    uri = "/submit/responses/"
    data = {
        "url": path,
        "metadata": metadata or {},
        "feedback_form": feedback_form_id,
        "first_prompt_response": {
            "prompt": first_prompt_id,
            # "response": first_prompt_id,  # TODO: Is this correct?
            "value": first_prompt_value,
        },
    }
    response = feedback_api_client().post(uri, data)
    print(f"Response: {response}")
    return response


def submit_additional_feedback(response_id, prompt_id, prompt_value):
    uri = "/submit/prompt-responses/"
    data = {
        "prompt": prompt_id,
        "response": response_id,
        "value": prompt_value,
    }
    return feedback_api_client().post(uri, data)
