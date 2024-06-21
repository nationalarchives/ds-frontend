from flask import Blueprint

bp = Blueprint("wagtail", __name__)

from app.wagtail import routes  # noqa: E402,F401
