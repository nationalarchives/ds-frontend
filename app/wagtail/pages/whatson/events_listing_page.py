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
        events=events_list.get("items", []),
    )
