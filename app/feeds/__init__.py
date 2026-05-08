from flask import Blueprint

bp = Blueprint("feeds", __name__)

from app.feeds import routes
