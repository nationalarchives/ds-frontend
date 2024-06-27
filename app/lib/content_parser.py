import re

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
