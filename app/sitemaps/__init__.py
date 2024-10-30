from flask import Blueprint

bp = Blueprint("sitemaps", __name__)

from app.sitemaps import routes  # noqa: E402,F401
