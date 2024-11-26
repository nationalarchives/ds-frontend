from flask import Blueprint

bp = Blueprint("site_search", __name__)

from app.site_search import routes  # noqa: E402,F401
