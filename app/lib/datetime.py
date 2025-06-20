from datetime import datetime


def get_date_from_string(s):  # noqa: C901
    if not s:
        return None
    try:
        return datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError:
        pass
    try:
        return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        pass
    try:
        return datetime.strptime(s, "%Y-%m-%dT%H:%M:%S%z")
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
