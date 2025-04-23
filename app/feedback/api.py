from app.lib.api import JSONAPIClient
from flask import current_app


def feedback_api_client():
    api_url = current_app.config.get("FEEDBACK_API_URL")
    api_key = current_app.config.get("FEEDBACK_API_KEY")
    if not api_url or not api_key:
        current_app.logger.error("FEEDBACK_API_URL or FEEDBACK_API_KEY not set")
        raise Exception("FEEDBACK_API_URL or FEEDBACK_API_KEY not set")
    client = JSONAPIClient(api_url)
    client.add_header("Authorization", f"Token {api_key}")
    return client


def page_feedback_form(path):
    if project_id := current_app.config.get("FEEDBACK_PROJECT_ID"):
        uri = f"/core/projects/{project_id}/feedback-forms/path{path}"
        return feedback_api_client().get(uri)
    return []


def page_feedback_form_by_id(form_id):
    if project_id := current_app.config.get("FEEDBACK_PROJECT_ID"):
        uri = f"/core/projects/{project_id}/feedback-forms/{form_id}/"
        return feedback_api_client().get(uri)
    return []


def submit_first_feedback(
    path, feedback_form_id, first_prompt_id, first_prompt_value, metadata={}
):
    uri = "/submit/responses/"
    data = {
        "url": path,
        "metadata": metadata,
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
