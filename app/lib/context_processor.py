import calendar
import json
from datetime import datetime
from urllib.parse import unquote

from app.lib import cache
from flask import request


def now_iso_8601():
    now = datetime.now()
    now_date = now.strftime("%Y-%m-%dT%H:%M:%SZ")
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


def pretty_date_range(s_from, s_to):
    date_from = get_date_from_string(s_from)
    date_to = get_date_from_string(s_to)
    if date_from and date_to:
        date_to_string = date_to.strftime("%d %B %Y")
        if (
            date_from.day == 1
            and date_from.month == 1
            and (
                (date_to.day == 31 and date_to.month == 12)
                or (date_to.day == 1 and date_to.month == 1)
            )
        ):
            if date_from.year == date_to.year:
                return date_from.year
            return f"{date_from.year}–{date_to.year}"
        if date_from.year == date_to.year:
            if date_from.month == date_to.month:
                if date_from.day == date_to.day:
                    return date_from.strftime("%d %B %Y")
                else:
                    return f"{date_from.strftime('%d')}–{date_to_string}"
            else:
                return f"{date_from.strftime('%d %B')} to {date_to_string}"
        else:
            return f"{date_from.strftime('%d %B %Y')} to {date_to_string}"
    if date_from:
        return f"From {date_from.strftime('%d %B %Y')}"
    if date_to:
        return f"To {date_to.strftime('%d %B %Y')}"
    return f"{s_from}–{s_to}"


@cache.cached(timeout=3600, key_prefix="logo_adornment")
def logo_adornment():
    now = datetime.now()
    now_day = now.day
    now_month = now.month
    now_year = now.year

    cal = calendar.Calendar(firstweekday=calendar.MONDAY)
    november_calendar_this_year = cal.monthdatescalendar(now.year, 11)
    second_sunday_in_november_this_year = [
        day
        for week in november_calendar_this_year
        for day in week
        if day.weekday() == calendar.SUNDAY and day.month == 11
    ][1].day

    if (
        now_month == 11
        and now_day >= 2
        and (now_day <= max(11, second_sunday_in_november_this_year))
    ):
        return "remembrance"
    elif now_month == 2:
        return "progress"
    elif now_month == 6:
        return "pride"
    elif now_month == 10:
        return "black_history"
    elif now_day == 15 and now_month == 3 and now_year == 2025:
        return "comic_relief"
    elif now_day == 22 and now_month == 4 and now_year == 2025:
        return "earth_day"
    return ""
