import json
from datetime import datetime
from urllib.parse import unquote

from app.lib.datetime import get_date_from_string
from flask import current_app, request


def now_iso_8601():
    now = datetime.now()
    now_date = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    return now_date


def now_iso_8601_no_time():
    now = datetime.now()
    now_date = now.strftime("%Y-%m-%d")
    return now_date


def now_rfc_822():
    now = datetime.now()
    now_date = now.strftime("%a, %-d %b %Y %H:%M:%S GMT")
    return now_date


def cookie_preference(policy):
    if "cookies_policy" in request.cookies:
        cookies_policy = request.cookies["cookies_policy"]
        preferences = json.loads(unquote(cookies_policy))
        return preferences[policy] if policy in preferences else None
    return None


def pretty_date_range(
    s_from, s_to, omit_days=False, show_time=False, sentence_case=False
):
    date_from = get_date_from_string(s_from)
    date_to = get_date_from_string(s_to)
    if date_from and date_to:
        date_to_string = date_to.strftime("%B %Y" if omit_days else "%-d %B %Y")
        if (
            date_from.day == 1
            and date_from.month == 1
            and date_to.day == 31
            and date_to.month == 12
        ):
            if date_from.year == date_to.year:
                return str(date_from.year)
            return f"{date_from.year} to {date_to.year}"
        if date_from.year == date_to.year:
            if date_from.month == date_to.month:
                if date_from.day == date_to.day:
                    if show_time:
                        if (
                            date_from.hour == date_to.hour
                            and date_from.minute == date_to.minute
                        ):
                            return date_from.strftime("%-d %B %Y, %H:%M")
                        return f"{date_from.strftime('%-d %B %Y, %H:%M')} to {date_to.strftime('%H:%M')}"
                    return date_from.strftime("%B %Y" if omit_days else "%-d %B %Y")
                if omit_days:
                    return date_to_string
                return f"{date_from.strftime('%-d')} to {date_to_string}"
            return f"{date_from.strftime('%B' if omit_days else "%-d %B")} to {date_to_string}"
        return f"{date_from.strftime('%B %Y' if omit_days else "%-d %B %Y")} to {date_to_string}"
    if date_from:
        start = "from" if sentence_case else "From"
        return f"{start} {date_from.strftime('%B %Y' if omit_days else "%-d %B %Y")}"
    if date_to:
        start = "now to" if sentence_case else "Now to"
        return f"{start} {date_to.strftime('%B %Y' if omit_days else "%-d %B %Y")}"
    return f"{s_from} to {s_to}"


def is_today_in_date_range(s_from, date_to):
    date_from = datetime.strptime(s_from, "%Y-%m-%d").date()
    date_to = datetime.strptime(date_to, "%Y-%m-%d").date()
    today = datetime.now().date()
    return date_from <= today <= date_to


def display_phase_banner():
    return any(
        request.path.startswith(uri)
        for uri in current_app.config.get("SHOW_PHASE_BANNER_ON_URIS", [])
    )
