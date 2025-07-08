from app.wagtail.api import page_children
from flask import render_template


def whats_on_index_page(page_data):
    all_children = page_children(page_data["id"]).get("items", [])
    groups = {
        "children": {
            "title": "Event types",
            "items": [],
        },
        "series": {
            "title": "Events by series",
            "card_supertitle": "Event series",
            "items": [],
        },
        "categories": {
            "title": "Events by format",
            "card_supertitle": "Event format",
            "items": [],
        },
        "dates": {
            "title": "Events by date",
            "items": [],
        },
        "locations": {
            "title": "Events by location",
            "card_supertitle": "Event location",
            "items": [],
        },
    }
    for page in all_children:
        print(f"Processing page: {page['title']} ({page['type']})")
        if page["type"] in [
            "whatson.EventsListingPage",
            "whatson.ExhibitionsListingPage",
        ]:
            groups["children"]["items"].append(page)
        elif page["type"] == "whatson.WhatsOnSeriesPage":
            groups["series"]["items"].append(page)
        elif page["type"] == "whatson.WhatsOnCategoryPage":
            groups["categories"]["items"].append(page)
        elif page["type"] == "whatson.WhatsOnDateListingPage":
            groups["dates"]["items"].append(page)
        elif page["type"] == "whatson.WhatsOnLocationListingPage":
            groups["locations"]["items"].append(page)
    return render_template(
        "whats_on/index.html",
        page_data=page_data,
        groups=groups,
    )
