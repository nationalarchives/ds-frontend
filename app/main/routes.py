from flask import render_template

from app.lib import cache
from app.main import bp


@bp.route("/")
@cache.cached()
def hello_world():
    return render_template("home.html")


@bp.route("/healthcheck/live")
def healthcheck():
    return "ok"
