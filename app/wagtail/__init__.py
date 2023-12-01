from flask import Blueprint

from ..lib.breadcrumbs import breadcrumbs

bp = Blueprint("wagtail", __name__)

from app.wagtail import routes  # noqa: E402,F401
