from app.lib import cache
from app.main import bp
from flask import render_template


@bp.route("/")
@cache.cached()
def home():
    return render_template("main/home.html")


@bp.route("/accessibility")
@cache.cached()
def accessibility():
    return render_template("main/accessibility.html")


@bp.route("/cookies")
@cache.cached()
def cookies():
    return render_template("main/cookies.html")


@bp.route("/healthcheck/live")
def healthcheck():
    return "ok"
