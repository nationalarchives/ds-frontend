from flask import Blueprint

bp = Blueprint("error_pages", __name__)

from app.error_pages import routes
