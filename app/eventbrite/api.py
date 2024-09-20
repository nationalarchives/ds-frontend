import requests
from app.lib.api import ApiResourceNotFound
from flask import current_app


def eventbrite_api_request_handler(uri, params={}):
    api_url = current_app.config.get("EVENTBRITE_API_URL")
    params["token"] = current_app.config.get("EVENTBRITE_API_PRIVATE_TOKEN")
    url = f"{api_url}/{uri}"
    current_app.logger.debug(f"API endpoint requested: {url} (params {params})")
    r = requests.get(url, params=params)
    if r.status_code == 404:
        current_app.logger.warning(f"Resource not found: {url}")
        raise ApiResourceNotFound("Resource not found")
    if r.status_code == requests.codes.ok:
        try:
            return r.json()
        except requests.exceptions.JSONDecodeError:
            current_app.logger.error("API provided non-JSON response")
            raise ConnectionError("API provided non-JSON response")
    current_app.logger.error(
        f"API responded with {r.status_code} status for {url}"
    )
    raise ConnectionError("Request to API failed")


def tna_events(page, children_per_page, params={}):
    uri = "organizations/32190014757/events/"  # TODO
    params = params | {
        "page": page,
        "page_size": children_per_page,
        "order_by": "start_asc",
        "status": "live",
        "time_filter": "current_future",
        "expand": "logo,venue,ticket_availability,logo",
    }
    return eventbrite_api_request_handler(uri, params)


def event_details(event_id, params={}):
    uri = f"events/{event_id}"
    params = params | {
        "expand": "logo,venue,ticket_availability,logo,organizer,checkout_settings"
    }
    return eventbrite_api_request_handler(uri, params)
