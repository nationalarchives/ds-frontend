import re
import urllib.parse
from datetime import datetime

from app.lib.util import strtobool
from flask import url_for


def tna_html(s):
    return s.replace("<ul>", '<ul class="tna-ul">').replace(
        "<ol>", '<ol class="tna-ol">'
    )


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


def article_supertitle(s):
    if s == "articles.ArticlePage":
        return "The story of"
    if s == "articles.FocusedArticlePage":
        return "Focus on"
    if s == "articles.RecordArticlePage":
        return "Record revealed"
    if s == "collections.HighlightGalleryPage":
        return "Gallery"
    return ""


def article_type(s):
    if s == "articles.ArticlePage" or s == "articles.FocusedArticlePage":
        return "Article"
    if s == "articles.RecordArticlePage":
        return "Records revealed"
    if s == "collections.HighlightGalleryPage":
        return "Gallery"
    if s == "collections.TimePeriodExplorerPage":
        return "Time period"
    if s == "collections.TopicExplorerPage":
        return "Topic"
    return ""


def brand_icon_from_url(s):
    if "facebook.com" in s:
        return "facebook"
    if "youtube.com" in s:
        return "youtube"
    return ""


def headings_list(s):
    headings_raw = re.findall(
        r'<h([1-6])[^>]*id="([\w\-]+)"[^>]*>\s*([\w\s\.]+)\s*<', s
    )
    headings = [
        {
            "title": heading[2],
            "id": heading[1],
            "level": heading[0],
            "children": [],
        }
        for heading in headings_raw
    ]
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
    ext_ref_pattern = re.compile(r'(<a class="extref" href="([\w\d\-]+)">)')
    for link, id in re.findall(ext_ref_pattern, s):
        new_link = url_for("catalogue.details", id=id)
        s = s.replace(link, f'<a href="{new_link}">')
    return s


def remove_all_whitespace(s):
    return s.replace(" ", "")


def url_encode(s):
    return urllib.parse.quote(s, safe="")


def to_bool(s):
    return strtobool(s) if s else False
