import re

from app.lib.abbreviations import abbreviations
from flask import render_template


def b_to_strong(html):
    html = html.replace("<b>", "<strong>")
    html = html.replace("<b ", "<strong ")
    html = html.replace("</b>", "</strong>")
    return html


def lists_to_tna_lists(html):
    html = html.replace("<ul>", '<ul class="tna-ul">')
    # html = re.sub(r'<ul( class="([^"]*)")?>', r'<ul class="tna-ul \g<2>">', html)
    html = html.replace("<ol>", '<ol class="tna-ol">')
    return html


def strip_wagtail_attributes(html):
    html = re.sub(r' data-block-key="([^"]*)"', "", html)
    return html


def replace_line_breaks(html):
    html = html.replace("\r\n", "<br>")
    return html


def add_abbreviations(html):
    for item in abbreviations:
        html = re.sub(
            r"([ '\(\"])%s([ ,;<'\"\.\)])" % item[0],
            r"\g<1>" + f'<abbr title="{item[1]}">{item[0]}</abbr>' r"\g<2>",
            html,
        )
    return html
