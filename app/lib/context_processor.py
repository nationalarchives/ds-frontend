from datetime import datetime


def merge_dict(dict, new_data):
    return dict | new_data


def merge_dict_if(dict, new_data, condition):
    return dict | new_data if condition else dict


def now_iso_8601():
    now = datetime.now()
    now_date = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    return now_date


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
