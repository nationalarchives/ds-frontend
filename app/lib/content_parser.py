from flask import render_template


def b_to_strong(html):
    html = html.replace("<b>", "<strong>")
    html = html.replace("</b>", "</strong>")
    return html


def lists_to_tna_lists(html):
    html = html.replace("<ul>", '<ul class="tna-ul">')
    html = html.replace("<ol>", '<ol class="tna-ol">')
    return html


def wagtail_api_table_to_html(table_data):
    return render_template("blocks/table.html", data=table_data)
