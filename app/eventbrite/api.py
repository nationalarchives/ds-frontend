import calendar
import datetime

import requests
from app.lib.api import ResourceNotFound
from flask import current_app


def eventbrite_api_request_handler(uri, params={}):
    api_url = current_app.config.get("EVENTBRITE_API_URL")
    params["token"] = current_app.config.get("EVENTBRITE_API_PRIVATE_TOKEN")
    url = f"{api_url}/{uri}"
    current_app.logger.debug(f"API endpoint requested: {url} (params {params})")
    r = requests.get(url, params=params)
    if r.status_code == 404:
        current_app.logger.warning(f"Resource not found: {url}")
        raise ResourceNotFound("Resource not found")
    if r.status_code == requests.codes.ok:
        try:
            return r.json()
        except requests.exceptions.JSONDecodeError:
            current_app.logger.error("API provided non-JSON response")
            raise ConnectionError("API provided non-JSON response")
    current_app.logger.error(f"API responded with {r.status_code} status for {url}")
    raise ConnectionError("Request to API failed")


def tna_events(page, children_per_page, params={}):
    uri = "organizations/32190014757/events/"  # TODO
    params.update(
        {
            "page": page,
            "page_size": children_per_page,
            "order_by": "start_asc",
            "status": "live",
            "expand": "logo,venue,ticket_availability,logo",
        }
    )
    if "start_date.range_start" not in params and "start_date.range_end" not in params:
        params.update(
            {
                "time_filter": "current_future",
            }
        )
    return eventbrite_api_request_handler(uri, params)


def tna_events_by_date(
    page, children_per_page, year=None, month=None, day=None, params={}
):
    now = datetime.datetime.now()
    start = {
        "year": now.year,
        "month": now.month,
        "day": now.day,
    }
    end = {
        "year": now.year,
        "month": now.month,
        "day": now.day,
    }
    if year:
        start.update({"year": year})
        end.update({"year": year})
    else:
        start.update({"year": now.year})
        end.update({"year": now.year})
    if month:
        start.update({"month": month})
        end.update({"month": month})
        if day:
            start.update({"day": day})
            end.update({"day": day})
        else:
            start.update({"day": "01"})
            end.update({"day": calendar.monthrange(int(end["year"]), int(month))[1]})
    else:
        if day:
            start.update({"month": now.month})
            end.update({"month": now.month})
            start.update({"day": day})
            end.update({"day": day})
        else:
            start.update({"day": "01"})
            end.update({"day": calendar.monthrange(now.year, now.month)[1]})
    # print(
    #     f"From {str(start['year']).rjust(2, "0")}-{str(start['month']).rjust(2, "0")}-{str(start['day']).rjust(2, "0")} to {str(end['year']).rjust(2, "0")}-{str(end['month']).rjust(2, "0")}-{str(end['day']).rjust(2, "0")}"
    # )
    return tna_events(
        page,
        children_per_page,
        {
            "start_date.range_start": f"{str(start['year']).rjust(2, "0")}-{str(start['month']).rjust(2, "0")}-{str(start['day']).rjust(2, "0")}",
            "start_date.range_end": f"{str(end['year']).rjust(2, "0")}-{str(end['month']).rjust(2, "0")}-{str(end['day']).rjust(2, "0")}",
            **params,
        },
    )


def event_details(event_id, params={}):
    uri = f"events/{event_id}"
    params.update(
        {"expand": "logo,venue,ticket_availability,logo,organizer,checkout_settings"}
    )
    return eventbrite_api_request_handler(uri, params)
