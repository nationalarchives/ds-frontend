import json
from datetime import datetime
from urllib.parse import unquote

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


def get_date_from_string(s):
    try:
        return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        pass
    try:
        return datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        pass
    try:
        return datetime.strptime(s, "%Y-%m")
    except ValueError:
        pass
    try:
        return datetime.strptime(s, "%Y")
    except ValueError:
        pass
    return None


def pretty_date_range(s_from, s_to, show_days=True):
    date_from = get_date_from_string(s_from)
    date_to = get_date_from_string(s_to)
    if date_from and date_to:
        date_to_string = date_to.strftime("%-d %B %Y" if show_days else "%B %Y")
        if (
            date_from.day == 1
            and date_from.month == 1
            and date_to.day == 31
            and date_to.month == 12
        ):
            if date_from.year == date_to.year:
                return str(date_from.year)
            return f"{date_from.year}–{date_to.year}"
        if date_from.year == date_to.year:
            if date_from.month == date_to.month:
                if date_from.day == date_to.day:
                    return date_from.strftime("%-d %B %Y" if show_days else "%B %Y")
                elif show_days:
                    return f"{date_from.strftime('%-d')}–{date_to_string}"
                else:
                    return date_to_string
            else:
                return f"{date_from.strftime('%-d %B' if show_days else "%B")} to {date_to_string}"
        else:
            return f"{date_from.strftime('%-d %B %Y' if show_days else "%B %Y")} to {date_to_string}"
    if date_from:
        return f"From {date_from.strftime('%-d %B %Y' if show_days else "%B %Y")}"
    if date_to:
        return f"To {date_to.strftime('%-d %B %Y' if show_days else "%B %Y")}"
    return f"{s_from}–{s_to}"


def display_phase_banner():
    return any(
        request.path.startswith(uri)
        for uri in current_app.config.get("SHOW_PHASE_BANNER_ON_URIS", [])
    )
