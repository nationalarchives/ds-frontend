import requests
from flask import render_template, request

from app.explore import bp
from app.lib import cache, page_details, page_details_by_uri
from app.wagtail import breadcrumbs

from .render import render_explore_page


@bp.route("/")
@cache.cached()
def explore():
    try:
        explore_data = page_details(5)
        large_cards_data = explore_data["body"][0]["value"]
        large_card_1 = page_details(large_cards_data["page_1"])
        large_card_2 = page_details(large_cards_data["page_2"])
    except ConnectionError:
        return render_template("errors/api.html"), 502
    except Exception:
        return render_template("errors/page-not-found.html"), 404
    return render_template(
        "explore/index.html",
        breadcrumbs=breadcrumbs(explore_data["id"]),
        data=explore_data,
        large_cards=[large_card_1, large_card_2],
    )


@bp.route("/<path:path>/")
@cache.cached()
def explore_page(path):
    try:
        page_data = page_details_by_uri(request.path)
    except ConnectionError:
        return render_template("errors/api.html"), 502
    except Exception:
        return render_template("errors/page-not-found.html"), 404
    return render_explore_page(page_data)
