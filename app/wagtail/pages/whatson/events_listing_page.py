import datetime

from app.lib.template_filters import qs_active, qs_update
from app.wagtail.api import events
from flask import render_template, request


def events_listing_page(page_data):
    event_params = {}
    date_error = None
    location_quick_filters = [
        {
            "label": "Any location",
            "href": "?" + qs_update(request.args, "location", "all"),
            "selected": qs_active(request.args, "location", "all")
            or not request.args.get("location"),
        },
        {
            "label": "At The National Archives",
            "href": "?" + qs_update(request.args, "location", "at_tna"),
            "selected": qs_active(request.args, "location", "at_tna"),
        },
        {
            "label": "Online",
            "href": "?" + qs_update(request.args, "location", "online"),
            "selected": qs_active(request.args, "location", "online"),
        },
    ]

    date_today = datetime.date.today()
    date_seven_days = date_today + datetime.timedelta(days=7)
    date_thirty_days = date_today + datetime.timedelta(days=30)

    date_from = request.args.get("date_from", None)
    date_from_date = None
    if date_from:
        date_from_date = datetime.datetime.strptime(date_from, "%Y-%m-%d").date()
    # elif "date_from" not in request.args:
    #     date_from_date = date_today
    #     date_from = date_from_date.strftime("%Y-%m-%d")

    date_to = request.args.get("date_to", None)
    date_to_date = (
        datetime.datetime.strptime(date_to, "%Y-%m-%d").date() if date_to else None
    )
    if date_from_date and date_to_date and date_from_date > date_to_date:
        date_error = "To date cannot be before from date"
        # date_to = None

    all_events = events(
        type=request.args.get("type", None),
        location=request.args.get("location", None),
        date_from=date_from,
        date_to=date_to,
        params=event_params,
    )

    return render_template(
        "whats_on/events.html",
        page_data=page_data,
        events=all_events.get("items", []),
        date_from=date_from,
        date_to=date_to,
        date_today=date_today.strftime("%Y-%m-%d"),
        date_seven_days=date_seven_days.strftime("%Y-%m-%d"),
        date_thirty_days=date_thirty_days.strftime("%Y-%m-%d"),
        date_error=date_error,
        location_quick_filters=location_quick_filters,
    )
