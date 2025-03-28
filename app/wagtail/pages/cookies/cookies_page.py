from app.wagtail.api import page_children
from flask import current_app, render_template


def cookies_page(page_data):
    details_page = None
    try:
        children_data = page_children(
            page_data["id"], {"type": "cookies.CookieDetailsPage", "limit": 1}
        )
        details_page = children_data["items"][0]
    except ConnectionError:
        current_app.logger.error(
            f"API error getting children for page {page_data['id']}"
        )
    except Exception:
        current_app.logger.error(
            f"Exception getting children for page {page_data['id']}"
        )
    return render_template(
        "main/cookies.html",
        page_data=page_data,
        details_page=details_page,
    )
