import re

from app.lib.abbreviations import abbreviations


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
    html = html.replace("<br/>", "<br>")
    html = html.replace("<br />", "<br>")
    return html


def add_rel_to_external_links(html):
    html = re.sub(
        r'<a href="(?!https:\/\/(www|discovery|webarchive)\.nationalarchives\.gov\.uk\/)',
        '<a rel="noreferrer nofollow noopener" href="',
        html,
    )
    return html


def replace_footnotes(html):
    html = re.sub(
        r'<footnote[^>]*id="([\w\d\-]+)"[^>]*>\s*\[([\w\d]+)\]\s*</footnote>',
        r'<sup data-footnoteid="\g<1>"><a href="#footnote-\g<1>" class="tna-footnote" title="Footnote \g<2>">[\g<2>]</a></sup>',
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
