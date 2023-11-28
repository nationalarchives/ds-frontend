from app.lib import cache
from app.main import bp
from flask import render_template


@bp.route("/")
@cache.cached()
def hello_world():
    return render_template("welcome.html")


@bp.route("/healthcheck/live")
def healthcheck():
    return "ok"
