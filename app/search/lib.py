from app.lib.query import remove_arg
from app.lib.template_filters import slugify
from flask import request


def get_filters(filters, args):
    return [
        {
            "title": filter["title"],
            "type": filter["type"],
            "slug": slugify(filter["title"]),
            "value": (
                args[slugify(filter["title"])]
                if filter["type"] == "text" and slugify(filter["title"]) in args
                else ""
            ),
            "options": (
                [
                    {
                        "text": option["name"],
                        "value": option["value"],
                        "checked": (
                            (
                                str(option["value"])
                                in args[slugify(filter["title"])]
                            )
                            if slugify(filter["title"]) in args
                            else False
                        ),
                        "remove_url": remove_arg(
                            request.args,
                            slugify(filter["title"]),
                            option["value"],
                        ),
                    }
                    for option in filter["options"]
                ]
                if filter["type"] == "multiple"
                else []
            ),
        }
        for filter in filters
    ]


def get_selected_filters(filters):
    selected_filters = []
    for filter in filters:
        if filter["type"] == "multiple":
            for option in filter["options"]:
                if option["checked"]:
                    selected_filters.append(
                        {
                            "group": filter["title"],
                            "filter": option["text"],
                            "remove_url": option["remove_url"],
                        }
                    )
        if filter["type"] == "text" and filter["value"]:
            selected_filters.append(
                {
                    "group": filter["title"],
                    "filter": filter["value"],
                    "remove_url": remove_arg(
                        request.args, slugify(filter["title"])
                    ),
                }
            )
    return selected_filters
