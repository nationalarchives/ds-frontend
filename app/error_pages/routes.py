from datetime import datetime

from flask import current_app, render_template, request
from markupsafe import escape
from tna_utilities.api import SimpleJsonApiClient
from tna_utilities.datetime import pretty_age, pretty_date
from tna_utilities.flask import do_not_cache

from app.error_pages import bp

ERROR_PAGE_TITLES = {
    "unknown_request": "The page you requested cannot be served",
    "restricted": "Restricted",
    "page_not_found": "Page not found",
    "page_archived": "Page no longer exists",
    "rate_limited": "Too many requests",
    "server": "There is a problem with the service",
    "service_down": "Service unavailable",
}


@bp.route("/400/")
@do_not_cache()
def bad_request_error():
    return render_template(
        "errors/unknown_request.html",
        status_code=400,
        pageTitle=ERROR_PAGE_TITLES["unknown_request"],
    ), 400


@bp.route("/401/")
@do_not_cache()
def unauthorized_error():
    return render_template(
        "errors/restricted.html",
        status_code=401,
        pageTitle=ERROR_PAGE_TITLES["restricted"],
    ), 401


@bp.route("/403/")
@do_not_cache()
def forbidden_error():
    return render_template(
        "errors/restricted.html",
        status_code=403,
        pageTitle=ERROR_PAGE_TITLES["restricted"],
    ), 403


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
            pageTitle=ERROR_PAGE_TITLES["page_archived"],
            status_code=410,
            archived_page_url=archived_page_url,
            last_archived_date=last_archived_date,
            last_archived_date_pretty=last_archived_date_pretty,
            last_archived_age=last_archived_age,
        ), 410
    except Exception:
        return render_template(
            "errors/page_not_found.html",
            status_code=404,
            pageTitle=ERROR_PAGE_TITLES["page_not_found"],
        ), 404


@bp.route("/405/")
@do_not_cache()
def method_not_allowed_error():
    return render_template(
        "errors/unknown_request.html",
        status_code=405,
        pageTitle=ERROR_PAGE_TITLES["unknown_request"],
    ), 405


@bp.route("/406/")
@do_not_cache()
def not_acceptable_error():
    return render_template(
        "errors/unknown_request.html",
        status_code=406,
        pageTitle=ERROR_PAGE_TITLES["unknown_request"],
    ), 406


@bp.route("/407/")
@do_not_cache()
def proxy_authentication_required_error():
    return render_template(
        "errors/restricted.html",
        status_code=407,
        pageTitle=ERROR_PAGE_TITLES["restricted"],
    ), 407


@bp.route("/410/")
@do_not_cache()
def gone_error():
    return page_not_found_error()


@bp.route("/414/")
@do_not_cache()
def uri_too_long_error():
    return render_template(
        "errors/unknown_request.html",
        status_code=414,
        pageTitle=ERROR_PAGE_TITLES["unknown_request"],
    ), 414


@bp.route("/429/")
@do_not_cache()
def too_many_requests_error():
    return render_template(
        "errors/rate_limited.html",
        status_code=429,
        pageTitle=ERROR_PAGE_TITLES["rate_limited"],
    ), 429


@bp.route("/500/")
@do_not_cache()
def server_error():
    return render_template(
        "errors/server.html", status_code=500, pageTitle=ERROR_PAGE_TITLES["server"]
    ), 500


@bp.route("/502/")
@do_not_cache()
def bad_gateway_error():
    return render_template(
        "errors/server.html", status_code=502, pageTitle=ERROR_PAGE_TITLES["server"]
    ), 502


@bp.route("/503/")
@do_not_cache()
def service_unavailable_error():
    return render_template(
        "errors/service-down.html",
        status_code=503,
        pageTitle=ERROR_PAGE_TITLES["service_down"],
    ), 503


@bp.route("/504/")
@do_not_cache()
def gateway_timeout_error():
    return render_template(
        "errors/server.html", status_code=504, pageTitle=ERROR_PAGE_TITLES["server"]
    ), 504
