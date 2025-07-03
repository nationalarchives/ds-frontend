import json
from datetime import datetime
from urllib.parse import unquote

from app.lib.datetime import get_date_from_string
from app.lib.template_filters import currency
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


def pretty_datetime_range(s_from, s_to, sentence_case=False):
    date_from = get_date_from_string(s_from)
    date_to = get_date_from_string(s_to)
    if date_from and date_to:
        if (
            date_from.year == date_to.year
            and date_from.month == date_to.month
            and date_from.day == date_to.day
        ):
            return (
                f"{date_from.strftime('%-d %B %Y, %H:%M')} to {date_to.strftime('%H:%M')}"
                if date_from.hour != date_to.hour or date_from.minute != date_to.minute
                else f"{date_from.strftime('%-d %B %Y, %H:%M')}"
            )
        return f"{date_from.strftime('%-d %B %Y, %H:%M')} to {date_to.strftime('%-d %B %Y, %H:%M')}"
    if date_from:
        start = "from" if sentence_case else "From"
        return f"{start} {date_from.strftime('%-d %B %Y, %H:%M')}"
    if date_to:
        start = "now to" if sentence_case else "Now to"
        return f"{start} {date_to.strftime('%-d %B %Y, %H:%M')}"
    return f"{s_from} to {s_to}"


def pretty_date_range(s_from, s_to, omit_days=False, sentence_case=False):
    date_from = get_date_from_string(s_from)
    date_to = get_date_from_string(s_to)
    if date_from and date_to:
        date_to_string = date_to.strftime("%B %Y" if omit_days else ("%-d %B %Y"))
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


def pretty_price_range(s_from, s_to):
    i_from = currency(s_from) if s_from else 0
    i_to = currency(s_to) if s_to else 0
    if i_from == 0 and i_to == 0:
        return "Free"
    if i_from == i_to:
        return f"£{i_from}"
    min_price = min(float(i_from), float(i_to))
    max_price = max(float(i_from), float(i_to))
    if min_price == 0:
        return f"Up to £{currency(max_price)}"
    return f"From £{currency(min_price)}"


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
