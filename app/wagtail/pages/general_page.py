from app.wagtail.api import breadcrumbs, page_children
from flask import current_app, render_template
from pydash import objects


def general_page(page_data):
    page_siblings = []
    if (True or page_data["show_siblings"]) and objects.get(
        page_data, "meta.parent.id"
    ):
        try:
            page_sibling_items = page_children(
                page_data["meta"]["parent"]["id"]
            )
            page_siblings = (
                page_sibling_items["items"]
                if "items" in page_sibling_items
                else []
            )
        except ConnectionError:
            current_app.logger.error(
                f"API error getting children for page {page_data['id']}"
            )
        except Exception:
            current_app.logger.error(
                f"Exception getting children for page {page_data['id']}"
            )
    return render_template(
        "main/general.html",
        breadcrumbs=breadcrumbs(page_data["id"]),
        page_data=page_data,
        page_siblings=page_siblings,
    )
