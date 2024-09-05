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


def replace_footnotes(html):
    # html = html.replace("</p>", f'<sup id="footnote-cite-{len(html)}"><a href="#footnote-{len(html)}" class="tna-footnote-cite">[abcdef]</a></sup></p>')  # TEMP
    # html = re.sub(r'<footnote[^>]*id="([\w\d\-]+)"[^>]*>\s*\[([\w\d]+)\]\s*</footnote>', r'<sup id="footnote-cite-\g<1>"><a href="#footnote-\g<1>" class="tna-footnote">\g<2></a></sup>', html)
    html = re.sub(
        r'<footnote[^>]*id="([\w\d\-]+)"[^>]*>\s*\[([\w\d]+)\]\s*</footnote>',
        r'<sup><a href="#footnote-\g<1>" class="tna-footnote">[\g<2>]</a></sup>',
        html,
    )
    return html


def add_abbreviations(html):
    for item in abbreviations:
        html = re.sub(
            r"([ '\(\"])%s([ ,;<'\"\.\)])" % item[0],
            r"\g<1>" + f'<abbr title="{item[1]}">{item[0]}</abbr>' r"\g<2>",
            html,
        )
    return html
