from app.wagtail.api import page_children
from flask import render_template


def whats_on_index_page(page_data):
    all_children = page_children(page_data["id"]).get("items", [])
    children = []
    series_pages = []
    category_pages = []
    for page in all_children:
        if page["type"] in [
            "whatson.EventsListingPage",
            "whatson.ExhibitionsListingPage",
        ]:
            children.append(page)
        elif page["type"] == "whatson.WhatsOnSeriesPage":
            series_pages.append(page)
        elif page["type"] == "whatson.WhatsOnCategoryPage":
            category_pages.append(page)
    return render_template(
        "whats_on/index.html",
        page_data=page_data,
        children=children,
        series_pages=series_pages,
        category_pages=category_pages,
    )
