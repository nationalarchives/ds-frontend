from flask import current_app, render_template

from app.error_pages.routes import api_error, server_error
from app.wagtail.api import page_children


def hub_page(page_data):
    children = []
    if not page_data["links"]:
        try:
            all_children = page_children(page_data["id"])
            children = all_children["items"]
        except ConnectionError:
            current_app.logger.exception(
                f"API error getting children for page {page_data['id']}"
            )
            return api_error()
        except Exception:
            current_app.logger.exception(
                f"Exception getting children for page {page_data['id']}"
            )
            return server_error()
    return render_template(
        "main/hub.html",
        page_data=page_data,
        children=children,
    )
