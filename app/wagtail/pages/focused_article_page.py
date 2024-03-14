from app.wagtail.api import breadcrumbs, page_details
from flask import render_template


def focused_article_page(page_data):
    topics = [
        {
            "href": topic["url"],
            "label": "Topic",
            "title": topic["title"],
            "src": topic["teaser_image_jpeg"]["full_url"],
            "alt": topic["teaser_image_jpeg"]["alt"],
            "width": topic["teaser_image_jpeg"]["width"],
            "height": topic["teaser_image_jpeg"]["height"],
        }
        for topic in page_data["topics"]
    ]
    time_periods = [
        {
            "href": time_period["url"],
            "label": "Time period",
            "title": time_period["title"],
            "src": time_period["teaser_image_jpeg"]["full_url"],
            "alt": time_period["teaser_image_jpeg"]["alt"],
            "width": time_period["teaser_image_jpeg"]["width"],
            "height": time_period["teaser_image_jpeg"]["height"],
        }
        for time_period in page_data["time_periods"]
    ]
    highlights = []
    if topics and time_periods:
        highlights = [topics[0], time_periods[0]]
    elif topics:
        highlights = [topics[0], topics[1]]
    elif time_periods:
        highlights = [time_periods[0], time_periods[1]]
    return render_template(
        "explore/focused-article.html",
        breadcrumbs=breadcrumbs(page_data["id"]),
        page_data=page_data,
        highlights=highlights,
    )
