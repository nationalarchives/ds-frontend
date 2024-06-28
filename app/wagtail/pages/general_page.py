from app.wagtail.api import breadcrumbs, page_children
from flask import current_app, render_template


def general_page(page_data):
    siblings = []
    if True or page_data["showSiblings"]:
        try:
            siblings = page_children(page_data["meta"]["parent"]["id"])
        except ConnectionError:
            current_app.logger.error(
                f"API error getting children for page {page_data['id']}"
            )
            return render_template("errors/api.html"), 502
        except Exception:
            current_app.logger.error(
                f"Exception getting children for page {page_data['id']}"
            )
            return render_template("errors/server.html"), 500
    return render_template(
        "main/general.html",
        breadcrumbs=breadcrumbs(page_data["id"]),
        page_data=page_data,
        siblings=siblings["items"],
    )
