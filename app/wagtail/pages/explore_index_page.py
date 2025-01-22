from app.lib.flagsmith import is_feature_enabled
from app.wagtail.api import breadcrumbs
from flask import render_template


def explore_index_page(page_data):
    return render_template(
        (
            "explore_the_collection/index_new.html"
            if is_feature_enabled("new_etc_landing_page")
            else "explore_the_collection/index.html"
        ),
        breadcrumbs=breadcrumbs(page_data["id"]),
        page_data=page_data,
    )
