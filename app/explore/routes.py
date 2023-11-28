import requests
from app.cms import breadcrumbs
from app.explore import bp
from app.lib import cache, page_deatils, page_deatils_by_uri
from flask import render_template, request

from .render import render_explore_page


@bp.route("/")
@cache.cached()
def explore():
    try:
        explore_data = page_deatils(5)
        large_cards_data = explore_data["body"][0]["value"]
        large_card_1 = page_deatils(large_cards_data["page_1"])
        large_card_2 = page_deatils(large_cards_data["page_2"])
    except ConnectionError:
        return render_template("errors/api.html"), 502
    except Exception:
        return render_template("errors/page-not-found.html"), 404
    return render_template(
        "explore.html",
        breadcrumbs=breadcrumbs(explore_data["id"]),
        data=explore_data,
        large_cards=[large_card_1, large_card_2],
    )


@bp.route("/<path:path>/")
@cache.cached()
def explore_page(path):
    try:
        page_data = page_deatils_by_uri(request.path)
    except ConnectionError:
        return render_template("errors/api.html"), 502
    except Exception:
        return render_template("errors/page-not-found.html"), 404
    return render_explore_page(page_data)
