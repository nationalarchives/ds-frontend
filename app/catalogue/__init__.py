from flask import Blueprint

bp = Blueprint("catalogue", __name__)

from app.catalogue import routes  # noqa: E402,F401
