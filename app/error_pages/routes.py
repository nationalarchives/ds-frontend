from datetime import datetime

from flask import current_app, render_template, request
from markupsafe import escape
from tna_utilities.api import SimpleJsonApiClient
from tna_utilities.datetime import pretty_age, pretty_date
from tna_utilities.flask import do_not_cache

from app.error_pages import bp


@bp.route("/400/")
@do_not_cache()
def bad_request_error():
    return render_template("errors/bad_request.html"), 400


@bp.route("/403/")
@do_not_cache()
def forbidden_error():
    return render_template("errors/forbidden.html"), 403


@bp.route("/404/")
@do_not_cache()
def page_not_found_error():
    client = SimpleJsonApiClient(current_app.config["WEBARCHIVE_CDXJ_API_URL"])
    url = request.url
    try:
        result = client.get(
            current_app.config["WEBARCHIVE_CDXJ_API_PATH"],
            params={
                "url": url,
                "output": "json",
                "filter": "status:200",
                "limit": 1,
                "sort": "reverse",
            },
        )
        last_archived_date = None
        last_archived_date_pretty = None
        last_archived_age = None
        if result and "timestamp" in result:
            timestamp = result["timestamp"]
            dt = datetime.strptime(timestamp, "%Y%m%d%H%M%S")
            last_archived_date = dt.strftime("%Y-%m-%d")
            last_archived_date_pretty = pretty_date(dt)
            last_archived_age = pretty_age(dt)
        archived_page_url = f"{current_app.config['WEBARCHIVE_BASE_URL']}/{escape(url)}"
        return render_template(
            "errors/page_archived.html",
            archived_page_url=archived_page_url,
            last_archived_date=last_archived_date,
            last_archived_date_pretty=last_archived_date_pretty,
            last_archived_age=last_archived_age,
        ), 410
    except Exception:
        return render_template("errors/page_not_found.html"), 404


@bp.route("/500/")
@do_not_cache()
def server_error():
    return render_template("errors/server.html"), 500


@bp.route("/502/")
@do_not_cache()
def api_error():
    return render_template("errors/api.html"), 502
