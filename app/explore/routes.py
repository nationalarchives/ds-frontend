import time

import requests
from app.cms import breadcrumbs
from app.explore import bp
from app.explore.render import render_explore_page
from app.lib import cache
from flask import render_template


@bp.route("/")
@cache.cached()
def explore():
    explore_data = requests.get(
        "http://host.docker.internal:8000/api/v2/pages/5/"
    ).json()
    large_cards = explore_data["body"][0]["value"]
    large_card_1 = requests.get(
        "http://host.docker.internal:8000/api/v2/pages/%d/"
        % (large_cards["page_1"])
    ).json()
    large_card_2 = requests.get(
        "http://host.docker.internal:8000/api/v2/pages/%d/"
        % (large_cards["page_2"])
    ).json()
    return render_template(
        "explore.html",
        breadcrumbs=breadcrumbs(explore_data["id"]),
        data=explore_data,
        large_cards=[large_card_1, large_card_2],
    )


@bp.route("/<path:path>/")
@cache.cached()
def explore_page(path):
    time.sleep(5)
    page_data = requests.get(
        "http://host.docker.internal:8000/api/v2/pages/find/?html_path=/explore-the-collection/%s/"
        % path
    ).json()
    return render_explore_page(page_data)
