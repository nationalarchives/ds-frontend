from app.wagtail.api import breadcrumbs, page_children
from flask import current_app, render_template


def hub_page(page_data):
    try:
        children = page_children(page_data["id"])
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
        "main/hub.html",
        breadcrumbs=breadcrumbs(page_data["id"]),
        page_data=page_data,
        children=children["items"],
    )
