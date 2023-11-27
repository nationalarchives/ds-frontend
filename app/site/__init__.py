from flask import Blueprint

bp = Blueprint("site", __name__)

from app.site import routes  # noqa: E402,F401
