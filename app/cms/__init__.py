from flask import Blueprint

from .breadcrumbs import breadcrumbs

bp = Blueprint("cms", __name__)

from app.cms import routes  # noqa: E402,F401
