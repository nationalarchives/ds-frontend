from datetime import datetime


def get_date_from_string(s):  # noqa: C901
    if not s:
        return None
    try:
        return datetime.fromisoformat(s)
    except ValueError:
        pass
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


def group_items_by_year_and_month(items, date_key):  # noqa: C901
    grouped = []
    for item in items.get("items", []):
        if request_date := item.get(date_key):
            try:
                request_datetime = datetime.fromisoformat(request_date)
            except ValueError:
                request_datetime = None
            if request_datetime:
                month = request_datetime.strftime("%B")
                year = request_datetime.strftime("%Y")
                year_index = next(
                    (i for i, d in enumerate(grouped) if d["heading"] == year), None
                )
                if year_index is None:
                    grouped.append(
                        {
                            "heading": year,
                            "items": [{"heading": month, "items": [item]}],
                        }
                    )
                else:
                    month_index = next(
                        (
                            i
                            for i, m in enumerate(grouped[year_index]["items"])
                            if m["heading"] == month
                        ),
                        None,
                    )
                    if month_index is None:
                        grouped[year_index]["items"].append(
                            {"heading": month, "items": [item]}
                        )
                    else:
                        grouped[year_index]["items"][month_index]["items"].append(item)
    return grouped
