import json
import re
import urllib.parse
from datetime import datetime

from flask import url_for

from .content_parser import (
    add_abbreviations,
    b_to_strong,
    lists_to_tna_lists,
    replace_line_breaks,
    strip_wagtail_attributes,
)


def tna_html(s):
    s = lists_to_tna_lists(s)
    s = b_to_strong(s)
    s = strip_wagtail_attributes(s)
    s = replace_line_breaks(s)
    s = add_abbreviations(s)
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
        r'<h([1-6])[^>]*id="([\w\d\-]+)"[^>]*>\s*([^<]+)\s*</', s
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


def parse_json(s):
    try:
        unquoted_string = urllib.parse.unquote(s)
        return json.loads(unquoted_string)
    except Exception:
        return {}


def wagtail_streamfield_contains_media(body):
    for body_item in body:
        if body_item["type"] == "content_section":
            for block in body_item["value"]["content"]:
                if block["type"] == "youtube_video" or block["type"] == "media":
                    return True
        elif (
            body_item["type"] == "youtube_video" or body_item["type"] == "media"
        ):
            return True
    return False


def sidebar_items_from_wagtail_body(body):
    page_sections = []
    for section in body:
        if section["type"] == "content_section":
            section_children = []
            section_grandchildren = []
            for block in reversed(section["value"]["content"]):
                if block["type"] == "sub_heading":
                    section_children.append(
                        {
                            "text": block["value"]["heading"],
                            "href": "#"
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
                            "href": "#"
                            + slugify(block["value"]["heading"])
                            + "-"
                            + block["id"],
                        }
                    )
            page_sections.append(
                {
                    "text": section["value"]["heading"],
                    "href": "#"
                    + slugify(section["value"]["heading"])
                    + "-"
                    + section["id"],
                    "children": (
                        reversed(section_children) if section_children else None
                    ),
                }
            )
    return page_sections


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
        classes = wagtail_cell_alignment_parser(
            cell["className"], cell_alignment_regex
        )
        alignment[cell["row"]][cell["col"]] = classes
    data = {"head": [], "body": [], "alignment": alignment}
    for row_index, row in enumerate(table_data["data"]):
        row_data = [
            {
                "head": (
                    column_index == 0 and table_data["first_col_is_header"]
                )
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
