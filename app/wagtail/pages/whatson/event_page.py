from app.lib.date_time import get_date_from_string
from flask import render_template


def event_page(page_data):
    sessions_by_date_unsorted = {}
    for session in page_data.get("sessions", []):
        date = get_date_from_string(session.get("start")).strftime("%Y-%m-%d")
        if date not in sessions_by_date_unsorted:
            sessions_by_date_unsorted[date] = []
        sessions_by_date_unsorted[date].append(session)
    sessions_by_date = []
    for date in sessions_by_date_unsorted.keys():
        sessions_by_date.append(
            {
                "date": date,
                "sessions": sorted(
                    sessions_by_date_unsorted[date],
                    key=lambda x: x.get("start"),
                ),
            }
        )
    sessions_by_date.sort(key=lambda x: x["date"])
    return render_template(
        "whats_on/event.html", page_data=page_data, sessions_by_date=sessions_by_date
    )
