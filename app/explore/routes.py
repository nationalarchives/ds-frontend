import requests
from app.explore import bp
from app.lib import cache, page_details, page_details_by_uri
from app.wagtail import breadcrumbs
from flask import render_template, request

from .render import render_explore_page


@bp.route("/")
@cache.cached()
def explore():
    try:
        explore_data = page_details(5)
        large_cards_data = explore_data["body"][0]["value"]
        large_card_1 = page_details(large_cards_data["page_1"])
        large_card_2 = page_details(large_cards_data["page_2"])
        featured_article = page_details(explore_data["featured_article"]["id"])
        featured_pages = [
            page_details(featured_page_id)
            for featured_page_id in explore_data["featured_articles"][0][
                "value"
            ]["items"]
        ]
    except ConnectionError:
        return render_template("errors/api.html"), 502
    except Exception:
        return render_template("errors/page-not-found.html"), 404
    large_cards = [
        {
            "href": card["meta"]["html_url"],
            "src": card["teaser_image_jpg"]["full_url"],
            "alt": card["teaser_image_jpg"]["alt"],
            "width": card["teaser_image_jpg"]["width"],
            "height": card["teaser_image_jpg"]["height"],
            "title": card["title"],
        }
        for card in [large_card_1, large_card_2]
    ]
    return render_template(
        "explore/index.html",
        breadcrumbs=breadcrumbs(explore_data["id"]),
        data=explore_data,
        large_cards=large_cards,
        featured_article=featured_article,
        featured_pages=featured_pages,
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
