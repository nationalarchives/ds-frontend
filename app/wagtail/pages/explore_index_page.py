from app.wagtail.api import breadcrumbs, page_details
from flask import render_template


def explore_index_page(page_data):
    try:
        large_cards_data = page_data["body"][0]["value"]
        large_card_1 = page_details(large_cards_data["page_1"]["id"])
        large_card_2 = page_details(large_cards_data["page_2"]["id"])
        featured_article = page_details(page_data["featured_article"]["id"])
        featured_pages = [
            page_details(featured_page["id"])
            for featured_page in page_data["featured_articles"][0]["value"][
                "items"
            ]
        ]
    except ConnectionError:
        return render_template("errors/api.html"), 502
    except Exception:
        return render_template("errors/page-not-found.html"), 404
    large_cards = [
        {
            "href": card["meta"]["html_url"],
            "src": card["teaser_image"]["image_jpeg"]["full_url"],
            # TODO
            # "alt": card["teaser_image"]["image_jpeg"]["alt"],
            "width": card["teaser_image"]["image_jpeg"]["width"],
            "height": card["teaser_image"]["image_jpeg"]["height"],
            "title": card["title"],
        }
        for card in [large_card_1, large_card_2]
    ]
    return render_template(
        "explore/index.html",
        breadcrumbs=breadcrumbs(page_data["id"]),
        page_data=page_data,
        large_cards=large_cards,
        featured_article=featured_article,
        featured_pages=featured_pages,
    )
