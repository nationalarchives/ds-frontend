from app.lib.query import remove_arg
from app.lib.template_filters import slugify
from flask import request


def get_filters(filters, args):
    filters_out = []
    for filter in filters:
        slug = slugify(filter["title"])
        type = filter["type"]
        filter_out = {
            "label": filter["title"],
            "type": type,
            "id": f"search-filter-{slug}",
            "name": f"{slug}[]" if type == "multiple" else slug,
        }
        if type == "text":
            filter_out["value"] = args[slug] if slug in args else ""
        elif type == "multiple":
            filter_out["items"] = [
                {
                    "text": option["name"],
                    "value": option["value"],
                    "checked": (
                        (str(option["value"]) in args[slug])
                        if slug in args
                        else False
                    ),
                    "remove_url": remove_arg(
                        request.args,
                        slug,
                        option["value"],
                    ),
                }
                for option in filter["options"]
            ]
            filter_out["small"] = True
        elif type == "daterange":
            filter_out["from"] = {
                "label": "From",
                "id": f"search-filter-{slug}-from",
                "name": "date-from",
            }
            filter_out["to"] = {
                "label": "To",
                "id": f"search-filter-{slug}-to",
                "name": "date-to",
            }
        filters_out.append(filter_out)
    return filters_out


def get_selected_filters(filters):
    selected_filters = []
    for filter in filters:
        if filter["type"] == "multiple":
            for option in filter["items"]:
                if option["checked"]:
                    selected_filters.append(
                        {
                            "group": filter["label"],
                            "filter": option["text"],
                            "remove_url": option["remove_url"],
                        }
                    )
        if filter["type"] == "text" and filter["value"]:
            selected_filters.append(
                {
                    "group": filter["label"],
                    "filter": filter["value"],
                    "remove_url": remove_arg(
                        request.args, slugify(filter["label"])
                    ),
                }
            )
    return selected_filters
