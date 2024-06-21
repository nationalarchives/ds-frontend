from flask import Blueprint

bp = Blueprint("legal", __name__)

from app.legal import routes  # noqa: E402,F401
