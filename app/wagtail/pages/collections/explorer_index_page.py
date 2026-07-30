from flask import render_template
from tna_utilities.flask import cacheable_duration


@cacheable_duration(3600)
def explorer_index_page(page_data):
    return render_template("explore_the_collection/index.html", page_data=page_data)
