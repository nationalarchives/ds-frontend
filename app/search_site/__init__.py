from flask import Blueprint

bp = Blueprint("search_site", __name__)

from app.search_site import routes  # noqa: E402,F401
