import math
from urllib.parse import unquote

from app.lib.pagination import pagination_object
from app.search import bp
from app.wagtail.api import global_alerts, search
from flask import render_template, request, url_for
from pydash import objects

"""
Align paths to routes in https://github.com/nationalarchives/ds-sitemap-search
"""


message = (
    "Replaced with the contents of ds-sitemap-search in dev, staging and production"
)


@bp.route("/")
def index():
    return message
