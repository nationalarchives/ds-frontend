import re
import urllib.parse
from datetime import datetime

from flask import url_for

from .content_parser import (
    b_to_strong,
    lists_to_tna_lists,
    strip_wagtail_attributes,
)


def tna_html(s):
    s = lists_to_tna_lists(s)
    s = b_to_strong(s)
    s = strip_wagtail_attributes(s)
    return s


def slugify(s):
    s = s.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_-]+", "-", s)
    s = re.sub(r"^-+|-+$", "", s)
    return s


def pretty_date(s):
    try:
        date = datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%fZ")
        return date.strftime("%d %B %Y")
    except ValueError:
        pass
    try:
        date = datetime.strptime(s, "%Y-%m-%d")
        return date.strftime("%d %B %Y")
    except ValueError:
        pass
    try:
        date = datetime.strptime(s, "%Y-%m")
        return date.strftime("%B %Y")
    except ValueError:
        pass
    try:
        date = datetime.strptime(s, "%Y")
        return date.strftime("%Y")
    except ValueError:
        pass
    return s


def iso_date(s):
    date = datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%fZ")
    new_date = date.strftime("%Y-%m-%dT%H:%M:%SZ")
    return new_date


def pretty_number(s):
    return f"{s:,}"


def headings_list(s):
    headings_regex = re.findall(
        r'<h([1-6])[^>]*id="([\w\-]+)"[^>]*>\s*([^<]+)\s*</', s
    )
    headings_raw = [
        {
            "text": heading[2],
            "href": "#" + heading[1],
            "level": int(heading[0]),
            "children": [],
        }
        for heading in headings_regex
    ]

    def group_headings(index, grouping):
        if index < len(headings_raw):
            next_heading = headings_raw[index]
            if len(grouping):
                prev_heading = grouping[-1]
                try:
                    if next_heading["level"] > prev_heading["level"]:
                        prev_heading["children"] = (
                            prev_heading["children"] or []
                        )
                        return group_headings(index, prev_heading["children"])
                    elif next_heading["level"] == prev_heading["level"]:
                        grouping.append(next_heading)
                        index = index + 1
                        return group_headings(index, grouping)
                    else:
                        raise Exception(
                            {"index": index, "heading": next_heading}
                        )
                except Exception as e:
                    (higher_heading,) = e.args
                    if (
                        higher_heading["heading"]["level"]
                        == prev_heading["level"]
                    ):
                        grouping.append(higher_heading["heading"])
                        higher_heading["index"] = higher_heading["index"] + 1
                        return group_headings(higher_heading["index"], grouping)
                    else:
                        raise Exception(higher_heading)
            else:
                grouping.append(next_heading)
                index = index + 1
                group_headings(index, grouping)
        return grouping

    headings = group_headings(0, [])
    return headings


def replace_ref(s):
    # TODO: Where do these link to?
    return s
    ext_ref_pattern = re.compile(
        r'(<span class="ref" (href="([\w\d\-]+)" )?target="([\w\d\-]+)">([^<]*)</span>)'
    )
    for link, href, href_value, target, text in re.findall(ext_ref_pattern, s):
        new_link = url_for("catalogue.details", id=target)
        s = s.replace(link, f'<a href="{new_link}">{text}</a>')
    return s


def replace_ext_ref(s):
    ext_ref_pattern = re.compile(r'(<a class="extref" href="([\w\d\-]+)\.?">)')
    for link, id in re.findall(ext_ref_pattern, s):
        new_link = url_for("catalogue.details", id=id)
        s = s.replace(link, f'<a href="{new_link}">')
    return s


def remove_all_whitespace(s):
    return s.replace(" ", "")


def url_encode(s):
    return urllib.parse.quote(s, safe="")
