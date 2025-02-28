import json
import math
import re
from datetime import datetime
from urllib.parse import unquote, urlencode, urlparse

from markupsafe import Markup

from .content_parser import (
    add_abbreviations,
    add_rel_to_external_links,
    b_to_strong,
    lists_to_tna_lists,
    replace_footnotes,
    replace_line_breaks,
    strip_wagtail_attributes,
)


def tna_html(s):
    if not s:
        return s
    s = lists_to_tna_lists(s)
    s = b_to_strong(s)
    s = strip_wagtail_attributes(s)
    s = replace_line_breaks(s)
    s = replace_footnotes(s)
    s = add_abbreviations(s)
    s = add_rel_to_external_links(s)
    return s


def slugify(s):
    if not s:
        return s
    s = s.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_-]+", "-", s)
    s = re.sub(r"^-+|-+$", "", s)
    return s


def seconds_to_time(s):
    if not s:
        return "00:00:00"
    total_seconds = int(s)
    hours = math.floor(total_seconds / 3600)
    minutes = math.floor((total_seconds - (hours * 3600)) / 60)
    seconds = total_seconds - (hours * 3600) - (minutes * 60)
    return f"{str(hours).rjust(2, '0')}:{str(minutes).rjust(2, '0')}:{str(seconds).rjust(2, '0')}"


def get_url_domain(s):
    try:
        domain = urlparse(s).netloc
        domain = re.sub(r"^www\.", "", domain)
        return domain
    except Exception:
        return s


def pretty_date(s, show_day=False):
    if not s:
        return s
    try:
        date = datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%fZ")
        return date.strftime("%A %-d %B %Y") if show_day else date.strftime("%-d %B %Y")
    except ValueError:
        pass
    try:
        date = datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")
        return date.strftime("%A %-d %B %Y") if show_day else date.strftime("%-d %B %Y")
    except ValueError:
        pass
    try:
        date = datetime.strptime(s, "%Y-%m-%d")
        return date.strftime("%A %-d %B %Y") if show_day else date.strftime("%-d %B %Y")
    except ValueError:
        pass
    try:
        date = datetime.strptime(s, "%Y-%m")
        return date.strftime("%A %B %Y") if show_day else date.strftime("%B %Y")
    except ValueError:
        pass
    try:
        date = datetime.strptime(s, "%Y")
        return date.strftime("%A %Y") if show_day else date.strftime("%Y")
    except ValueError:
        pass
    return s


def pretty_date_with_day(s):
    return pretty_date(s, True)


def currency(s):
    if not s:
        return "0"
    float_number = float(s)
    int_number = int(float_number)
    if int_number == float_number:
        return str(int_number)
    return str("%.2f" % float_number)


def rfc_822_format(s):
    if not s:
        return s
    try:
        date = datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%fZ")
        return date.strftime("%a, %-d %b %Y %H:%M:%S GMT")
    except ValueError:
        pass
    try:
        date = datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")
        return date.strftime("%a, %-d %b %Y %H:%M:%S GMT")
    except ValueError:
        pass
    return s


def headings_list(s):
    if not s:
        return s
    headings_regex = re.findall(
        r'<h([1-6])[^>]*id="([\w\d\-]+)"[^>]*>\s*(.+)\s*</h[1-6]>', s
    )
    headings_raw = [
        {
            "text": Markup(heading[2]),
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
                        prev_heading["children"] = prev_heading["children"] or []
                        return group_headings(index, prev_heading["children"])
                    elif next_heading["level"] == prev_heading["level"]:
                        grouping.append(next_heading)
                        index = index + 1
                        return group_headings(index, grouping)
                    else:
                        raise Exception({"index": index, "heading": next_heading})
                except Exception as e:
                    (higher_heading,) = e.args
                    if higher_heading["heading"]["level"] == prev_heading["level"]:
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


def parse_json(s):
    try:
        unquoted_string = unquote(s)
        return json.loads(unquoted_string)
    except Exception:
        return {}


def wagtail_streamfield_contains_media(body):
    for body_item in body:
        if body_item["type"] == "content_section":
            for block in body_item["value"]["content"]:
                if block["type"] == "youtube_video" or block["type"] == "media":
                    return True
        elif body_item["type"] == "youtube_video" or body_item["type"] == "media":
            return True
    return False


def sidebar_items_from_wagtail_body(content):
    body = content["body"]
    footnotes = content["footnotes"]
    page_sections = []
    page_children = []
    page_grandchildren = []
    for item in body:
        if item["type"] == "content_section":
            section_children = []
            section_grandchildren = []
            for block in reversed(item["value"]["content"]):
                if block["type"] == "sub_heading":
                    section_children.append(
                        {
                            "text": block["value"]["heading"],
                            "href": "#heading-"
                            + slugify(block["value"]["heading"])
                            + "-"
                            + block["id"],
                            "children": (
                                reversed(section_grandchildren)
                                if section_grandchildren
                                else None
                            ),
                        }
                    )
                    section_grandchildren = []
                elif block["type"] == "sub_sub_heading":
                    section_grandchildren.append(
                        {
                            "text": block["value"]["heading"],
                            "href": "#heading-"
                            + slugify(block["value"]["heading"])
                            + "-"
                            + block["id"],
                        }
                    )
            page_sections.append(
                {
                    "text": item["value"]["heading"],
                    "href": "#heading-"
                    + slugify(item["value"]["heading"])
                    + "-"
                    + item["id"],
                    "children": (
                        reversed(section_children) if section_children else None
                    ),
                }
            )
        # This shouldn't be needed as sub_headings can't yet go directly into the body
        elif item["type"] == "sub_heading":
            page_children.append(
                {
                    "text": item["value"]["heading"],
                    "href": "#heading-"
                    + slugify(item["value"]["heading"])
                    + "-"
                    + item["id"],
                    "children": (
                        reversed(page_grandchildren) if page_grandchildren else None
                    ),
                }
            )
            page_grandchildren = []
        # This shouldn't be needed as sub_sub_headings can't yet go directly into the body
        elif item["type"] == "sub_sub_heading":
            page_grandchildren.append(
                {
                    "text": item["value"]["heading"],
                    "href": "#heading-"
                    + slugify(item["value"]["heading"])
                    + "-"
                    + item["id"],
                }
            )
    if footnotes:
        page_sections.append(
            {
                "text": "Footnotes",
                "href": "#footnotes",
            }
        )
    return page_sections or page_children


def wagtail_table_parser(table_data):
    cell_alignment_regex = re.compile(r"^ht")

    def wagtail_cell_alignment_parser(classes, cell_alignment_regex):
        return [
            re.sub(cell_alignment_regex, "", class_name).lower()
            for class_name in classes.split(" ")
        ]

    alignment = [
        [[] for column in range(len(table_data["data"][0]))]
        for row in range(len(table_data["data"]))
    ]
    for cell in table_data["cell"]:
        classes = wagtail_cell_alignment_parser(cell["className"], cell_alignment_regex)
        alignment[cell["row"]][cell["col"]] = classes
    data = {"head": [], "body": [], "alignment": alignment}
    for row_index, row in enumerate(table_data["data"]):
        row_data = [
            {
                "head": (column_index == 0 and table_data["first_col_is_header"])
                or (row_index == 0 and table_data["first_row_is_table_header"]),
                "data": cell,
                "row_index": row_index,
                "column_index": column_index,
                "align": (alignment[row_index][column_index]),
            }
            for column_index, cell in enumerate(row)
        ]
        if row_index == 0 and table_data["first_row_is_table_header"]:
            data["head"].append(row_data)
        else:
            data["body"].append(row_data)
    return data


def qs_active(existing_qs, filter, by):
    """Active when identical key/value in existing query string."""
    qs_set = {(filter, str(by))}
    # Not active if either are empty.
    if not existing_qs or not qs_set:
        return False
    # See if the intersection of sets is the same.
    existing_qs_set = set(existing_qs.items())
    return existing_qs_set.intersection(qs_set) == qs_set


def qs_toggler(existing_qs, filter, by):
    """Resolve filter against an existing query string."""
    qs = {filter: by}
    # Don't change the currently rendering existing query string!
    rtn_qs = existing_qs.copy()
    # Test for identical key and value in existing query string.
    if qs_active(existing_qs, filter, by):
        # Remove so that buttons toggle their own value on and off.
        rtn_qs.pop(filter)
    else:
        # Update or add the query string.
        rtn_qs.update(qs)
    return urlencode(rtn_qs)


def qs_update(existing_qs, filter, value):
    rtn_qs = existing_qs.copy()
    rtn_qs.pop(filter)
    rtn_qs.update({filter: value})
    return urlencode(rtn_qs)
