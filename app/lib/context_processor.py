import json
from datetime import datetime
from urllib.parse import unquote

from app.lib.cache import cache
from flask import request


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


def get_date_from_datetime_string(s):
    try:
        return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        pass
    try:
        return datetime.strptime(s, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        pass
    return None


def get_date_from_date_string(s):
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


def get_year_from_date_string(s):
    if date := get_date_from_date_string(s):
        return date.strftime("%Y")
    if date := get_date_from_datetime_string(s):
        return date.strftime("%Y")
    return None


def get_month_year_from_date_string(s):
    if date := get_date_from_date_string(s):
        return date.strftime("%B %Y")
    if date := get_date_from_datetime_string(s):
        return date.strftime("%B %Y")
    return None


def pretty_date_range(s_from, s_to, show_days=True):
    show_time = False
    datetime_from = get_date_from_datetime_string(s_from)
    datetime_to = get_date_from_datetime_string(s_to)
    if datetime_from and datetime_to:
        show_time = True
        date_from = datetime_from
        date_to = datetime_to
    else:
        date_from = get_date_from_date_string(s_from)
        date_to = get_date_from_date_string(s_to)
    if date_from and date_to:
        date_to_string = date_to.strftime(
            "%-d %B %Y, %H:%M" if show_time else "%-d %B %Y" if show_days else "%B %Y"
        )
        if (
            date_from.day == 1
            and date_from.month == 1
            and date_to.day == 31
            and date_to.month == 12
        ):
            if date_from.year == date_to.year:
                return (
                    f"{date_from.strftime('%-d %B, %H:%M')} to {date_to_string}"
                    if show_time
                    else str(date_from.year)
                )
            return f"{date_from.year}–{date_to.year}"
        if date_from.year == date_to.year:
            if date_from.month == date_to.month:
                if date_from.day == date_to.day:
                    return (
                        f"{date_from.strftime('%-d %B %Y, %H:%M')}–{date_to.strftime('%H:%M')}"
                        if show_time
                        else date_from.strftime("%-d %B %Y" if show_days else "%B %Y")
                    )
                elif show_days:
                    return (
                        f"{date_from.strftime('%-d %B, %H:%M')} to {date_to_string}"
                        if show_time
                        else f"{date_from.strftime('%-d')}–{date_to_string}"
                    )
                else:
                    return date_to_string
            else:
                return (
                    f"{date_from.strftime('%-d %B, %H:%M')} to {date_to_string}"
                    if show_time
                    else f"{date_from.strftime('%-d %B' if show_days else "%B")} to {date_to_string}"
                )
        else:
            return (
                f"{date_from.strftime('%-d %B %Y, %H:%M')} to {date_to_string}"
                if show_time
                else f"{date_from.strftime('%-d %B %Y' if show_days else "%B %Y")} to {date_to_string}"
            )
    if date_from or datetime_from:
        return f"From {datetime_from.strftime("%-d %B %Y, %H:%M") if datetime_from else date_from.strftime("%-d %B %Y" if show_days else "%B %Y")}"
    if date_to or datetime_to:
        return f"To {datetime_to.strftime("%-d %B %Y, %H:%M") if datetime_to else date_to.strftime("%-d %B %Y" if show_days else "%B %Y")}"
    return f"{s_from}–{s_to}"
