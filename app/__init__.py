import json
import logging
import os
from urllib.parse import quote, unquote

import sentry_sdk
from flask import Flask, current_app, request
from jinja2 import ChoiceLoader, PackageLoader
from sentry_sdk.types import Event, Hint
from tna_utilities.string import slugify, unslugify

from app.lib.context_processor import (
    cookie_preference,
    display_phase_banner,
    is_today_in_date_range,
    now_iso_8601,
    now_iso_8601_date,
    now_rfc_822,
    pretty_date_range,
    pretty_datetime_range,
    pretty_price_range,
)
from app.lib.query import (
    qs_active,
    qs_remove,
    qs_toggler,
    qs_update,
)
from app.lib.talisman import talisman
from app.lib.template_filters import (
    currency,
    file_type_icon,
    get_url_domain,
    headings_list,
    is_today_or_future,
    month_year,
    multiline_address_to_single_line,
    number_to_text,
    parse_json,
    pretty_date,
    pretty_date_with_day,
    pretty_date_with_day_and_time,
    pretty_date_with_time,
    pretty_price,
    rfc_822_format,
    seconds_to_iso_8601_duration,
    seconds_to_time,
    sidebar_items_from_wagtail_streamfield,
    strip_day_from_date,
    strip_time_from_date,
    supertitle_from_domain,
    tna_html,
    url_encode,
    wagtail_streamfield_contains_code_block,
    wagtail_streamfield_contains_media,
    wagtail_table_parser,
)


def create_app(config_class):
    app = Flask(__name__, static_url_path="/static")
    app.config.from_object(config_class)

    if app.config["SENTRY_DSN"]:

        def before_send(event: Event, hint: Hint) -> Event | None:
            # Filter out preview page errors
            if event.get("transaction") == "wagtail.preview_page":
                return None
            return event

        sentry_sdk.init(
            dsn=app.config["SENTRY_DSN"],
            environment=app.config["ENVIRONMENT_NAME"],
            release=(
                f"ds-frontend@{app.config['BUILD_VERSION']}"
                if app.config["BUILD_VERSION"]
                else ""
            ),
            sample_rate=app.config["SENTRY_SAMPLE_RATE"],
            traces_sample_rate=app.config["SENTRY_SAMPLE_RATE"],
            profiles_sample_rate=app.config["SENTRY_SAMPLE_RATE"],
            before_send=before_send,
        )

    gunicorn_error_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers.extend(gunicorn_error_logger.handlers)
    app.logger.setLevel(
        gunicorn_error_logger.level or os.getenv("LOG_LEVEL", "warning").upper()
    )

    talisman.init_app(
        app,
        content_security_policy=app.config["CONTENT_SECURITY_POLICY"],
        allow_google_content_security_policy=True,
        force_https=app.config["FORCE_HTTPS"],
    )

    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True
    app.jinja_env.loader = ChoiceLoader(
        [
            PackageLoader("app"),
            PackageLoader("tna_frontend_jinja"),
        ]
    )

    @app.after_request
    def fix_http_only_cookies_preference(response):
        """
        TODO: Remove after 12 months (2027-06) when all incorrect cookies should have been set with the correct attributes.
        """
        cookie_preference_key = current_app.config["COOKIE_PREFERENCES_KEY"]
        if cookie_preference_key in request.cookies:
            value = request.cookies[cookie_preference_key]
            try:
                value_json = json.loads(unquote(value))
            except json.JSONDecodeError:
                value_json = {}
            if not isinstance(value_json, dict):
                value_json = {
                    "usage": False,
                    "settings": False,
                    "marketing": False,
                    "essential": True,
                }
            else:
                for key in {"usage", "settings", "marketing", "essential"}:
                    if key not in value_json:
                        value_json[key] = False if key != "essential" else True
            value = quote(json.dumps(value_json, separators=(",", ":")))
            response.set_cookie(
                cookie_preference_key,
                value,
                max_age=60 * 60 * 24 * 7,  # 7 days
                secure=True,
                samesite="Lax",
                httponly=False,
            )
        cookie_preference_set_key = current_app.config["COOKIE_PREFERENCES_SET_KEY"]
        if cookie_preference_set_key in request.cookies:
            value = (
                "true"
                if request.cookies[cookie_preference_set_key] == "true"
                else "false"
            )
            response.set_cookie(
                cookie_preference_set_key,
                value,
                max_age=60 * 60 * 24 * 7,  # 7 days
                secure=True,
                samesite="Lax",
                httponly=False,
            )
        return response

    filter_functions = [
        currency,
        file_type_icon,
        get_url_domain,
        supertitle_from_domain,
        headings_list,
        is_today_or_future,
        number_to_text,
        parse_json,
        pretty_date,
        pretty_date_with_day,
        pretty_date_with_time,
        pretty_date_with_day_and_time,
        strip_day_from_date,
        strip_time_from_date,
        month_year,
        multiline_address_to_single_line,
        pretty_price,
        rfc_822_format,
        seconds_to_iso_8601_duration,
        seconds_to_time,
        sidebar_items_from_wagtail_streamfield,
        slugify,
        tna_html,
        unslugify,
        url_encode,
        wagtail_streamfield_contains_code_block,
        wagtail_streamfield_contains_media,
        wagtail_table_parser,
    ]

    for filter_function in filter_functions:
        app.add_template_filter(filter_function)

    @app.context_processor
    def context_processor():
        return dict(
            cookie_preference=cookie_preference,
            display_phase_banner=display_phase_banner,
            now_iso_8601=now_iso_8601,
            now_iso_8601_date=now_iso_8601_date,
            now_rfc_822=now_rfc_822,
            pretty_date_range=pretty_date_range,
            pretty_datetime_range=pretty_datetime_range,
            pretty_price_range=pretty_price_range,
            is_today_in_date_range=is_today_in_date_range,
            qs_active=lambda filter_name, by: qs_active(
                request.args.to_dict(), filter_name, by
            ),
            qs_toggler=lambda filter_name, by: qs_toggler(
                request.args.to_dict(), filter_name, by
            ),
            qs_update=lambda filter_name, value: qs_update(
                request.args.to_dict(), filter_name, value
            ),
            qs_remove=lambda filter_name: qs_remove(
                request.args.to_dict(), filter_name
            ),
            app_config={
                "ENVIRONMENT_NAME": app.config["ENVIRONMENT_NAME"],
                "CONTAINER_IMAGE": app.config["CONTAINER_IMAGE"],
                "BUILD_VERSION": app.config["BUILD_VERSION"],
                "TNA_FRONTEND_VERSION": app.config["TNA_FRONTEND_VERSION"],
                "COOKIE_DOMAIN": app.config["COOKIE_DOMAIN"],
                "COOKIE_PREFERENCES_URL": app.config["COOKIE_PREFERENCES_URL"],
                "COOKIE_PREFERENCES_SET_KEY": app.config["COOKIE_PREFERENCES_SET_KEY"],
                "GA4_ID": app.config["GA4_ID"],
                "SENTRY_JS_ID": app.config["SENTRY_JS_ID"],
                "SENTRY_SAMPLE_RATE": app.config["SENTRY_SAMPLE_RATE"],
            },
            feature={
                "PHASE_BANNER": app.config["FEATURE_PHASE_BANNER"],
                "LOGO_ADORNMENTS_CSS": app.config["FEATURE_LOGO_ADORNMENTS_CSS"],
                "LOGO_ADORNMENTS_JS": app.config["FEATURE_LOGO_ADORNMENTS_JS"],
            },
        )

    from .feeds import bp as feeds_bp
    from .main import bp as site_bp
    from .search import bp as search_bp
    from .sitemaps import bp as sitemaps_bp
    from .wagtail import bp as wagtail_bp

    app.register_blueprint(site_bp)
    app.register_blueprint(sitemaps_bp)
    app.register_blueprint(feeds_bp, url_prefix="/feeds")
    app.register_blueprint(search_bp, url_prefix="/search")
    app.register_blueprint(wagtail_bp)

    return app
