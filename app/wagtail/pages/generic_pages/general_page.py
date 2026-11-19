from flask import current_app, render_template
from pydash import objects

from app.wagtail.api import page_children


def general_page(page_data):
    page_siblings = []
    if (
        page_data["page_sidebar"] == "pages"
        or page_data["page_sidebar"] == "pages_tabs"
    ) and objects.get(page_data, "meta.parent.id"):
        try:
            page_sibling_items = page_children(
                page_data["meta"]["parent"]["id"], limit=50
            )
            page_siblings = page_sibling_items.get("items", [])
        except ConnectionError:
            current_app.logger.exception(
                f"API error getting children for page {page_data['id']}"
            )
        except Exception:
            current_app.logger.exception(
                f"Exception getting children for page {page_data['id']}"
            )
    return render_template(
        "main/general.html",
        page_data=page_data,
        page_siblings=page_siblings,
    )
