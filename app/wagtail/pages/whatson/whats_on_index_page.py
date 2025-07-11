from app.wagtail.api import page_children
from flask import render_template


def whats_on_index_page(page_data):
    all_children = page_children(page_data["id"]).get("items", [])
    groups = {
        "children": {
            "title": "Browse what’s on",
            "items": [],
        },
        "series": {
            "title": "Browse by series",
            "card_supertitle": "Series",
            "items": [],
        },
        "categories": {
            "title": "Browse by format",
            "card_supertitle": "Format",
            "items": [],
        },
        "dates": {
            "title": "Browse by date",
            "items": [],
        },
        "locations": {
            "title": "Browse by location",
            "card_supertitle": "Location",
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
