from app.lib.api import ApiResourceNotFound, JSONAPIClient
from flask import current_app
from pydash import objects


def feedback_api_request_handler(uri, params={}):
    api_url = current_app.config.get("FEEDBACK_API_URL")
    if not api_url:
        current_app.logger.critical("FEEDBACK_API_URL not set")
        raise Exception("FEEDBACK_API_URL not set")
    client = JSONAPIClient(api_url)
    client.add_parameters(params)
    data = client.get(uri)
    return data


def get_prompts(page_uri, params={}):
    return {"id": "xyz789"}
    uri = "prompts/"
    params = params | {
        "page_uri": page_uri,
    }
    return feedback_api_request_handler(uri, params)


def submit_response_by_uri(page_uri, response=None, index=1):
    return {"feedback_id": "abc123"}


def submit_responses_by_uri(page_uri, responses=[]):
    return {"feedback_id": "abc123"}


def submit_response_by_feedback_id(feedback_id, response=None, index=1):
    return {}


def submit_responses_by_feedback_id(feedback_id, responses=[]):
    return {}
