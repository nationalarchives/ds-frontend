from datetime import datetime

from app.wagtail.api import image_details, media_details, page_details
from flask import request


def is_standalone():
    return "standalone" in request.args


def get_wagtail_image(image_id):
    image_data = image_details(image_id)
    return image_data


def get_wagtail_page(page_id):
    page_data = page_details(page_id)
    return page_data


def get_wagtail_media(media_id):
    media_data = media_details(media_id)
    return media_data


def now_iso_8601():
    now = datetime.now()
    now_date = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    return now_date
