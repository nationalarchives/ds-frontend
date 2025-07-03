import datetime

from app.lib.template_filters import qs_active, qs_remove, qs_update
from app.wagtail.api import events
from flask import render_template, request


def events_listing_page(page_data):
    time_period = request.args.get("date", "any")
    if time_period not in ["any", "today", "7days", "30days"]:
        return render_template("errors/page_not_found.html"), 400
    today = datetime.date.today()
    from_date = today.strftime("%Y-%m-%d")
    to_date = None
    if time_period == "today":
        to_date = from_date
    elif time_period == "7days":
        to_date = (today + datetime.timedelta(days=7)).strftime("%Y-%m-%d")
    elif time_period == "30days":
        to_date = (today + datetime.timedelta(days=30)).strftime("%Y-%m-%d")
    events_list = events(from_date=from_date, to_date=to_date)
    return render_template(
        "whats_on/events.html",
        page_data=page_data,
        time_period_selector=True,
        events=events_list.get("items", []),
    )


def events_listing_searchable_page(page_data):
    event_params = {}
    date_error = None
    if request.args.get("location") and request.args.get("location") not in [
        "at_tna",
        "online",
    ]:
        return render_template("errors/page_not_found.html"), 400
    location_quick_filters = [
        {
            "label": "Any location",
            "href": "?" + qs_remove(request.args, "location"),
            "selected": not request.args.get("location"),
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
        try:
            date_from_date = datetime.datetime.strptime(date_from, "%Y-%m-%d").date()
        except ValueError:
            date_from_date = None
            date_from = None

    date_to = request.args.get("date_to", None)
    try:
        date_to_date = (
            datetime.datetime.strptime(date_to, "%Y-%m-%d").date() if date_to else None
        )
    except ValueError:
        date_to_date = None
        date_to = None
    if date_from_date and date_to_date and date_from_date > date_to_date:
        date_error = "To date cannot be before from date"

    all_events = events(
        type=request.args.get("type", None),
        location=request.args.get("location", None),
        date_from=date_from,
        date_to=date_to,
        params=event_params,
    )

    return render_template(
        "whats_on/events-searchable.html",
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
