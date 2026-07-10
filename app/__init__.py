import logging
import os

import sentry_sdk
from flask import Flask, request
from jinja2 import ChoiceLoader, PackageLoader
from sentry_sdk.types import Event, Hint
from tna_utilities.string import slugify, unslugify
from tna_utilities.url import QueryStringTransformer

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
    qs_remove,
    qs_toggler,
    qs_update,
)
from app.lib.talisman import talisman
from app.lib.template_filters import (
    currency,
    domain_from_url,
    file_type_icon,
    headings_list,
    is_today_or_future,
    key_stage_ranges,
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
    app.jinja_env.add_extension("jinja2.ext.do")

    filter_functions = [
        currency,
        domain_from_url,
        file_type_icon,
        headings_list,
        is_today_or_future,
        key_stage_ranges,
        number_to_text,
        parse_json,
        pretty_date,
        pretty_date_with_day,
        pretty_date_with_day_and_time,
        pretty_date_with_time,
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
        supertitle_from_domain,
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
        qs = QueryStringTransformer(list(request.args.lists()))
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
            qs_is_value_in_parameter=lambda name, value: (
                qs.is_value_in_parameter(name, value)
                if qs.parameter_exists(name)
                else False
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
                "SIDEBAR_SCROLL_TOP_THRESHOLD": app.config[
                    "SIDEBAR_SCROLL_TOP_THRESHOLD"
                ],
            },
            feature={
                "PHASE_BANNER": app.config["FEATURE_PHASE_BANNER"],
                "LOGO_ADORNMENTS_CSS": app.config["FEATURE_LOGO_ADORNMENTS_CSS"],
                "LOGO_ADORNMENTS_JS": app.config["FEATURE_LOGO_ADORNMENTS_JS"],
            },
        )

    from .error_pages import bp as error_pages_bp
    from .feeds import bp as feeds_bp
    from .main import bp as main_bp
    from .search import bp as search_bp
    from .sitemaps import bp as sitemaps_bp
    from .wagtail import bp as wagtail_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(sitemaps_bp)
    app.register_blueprint(error_pages_bp, url_prefix="/error")
    app.register_blueprint(feeds_bp, url_prefix="/feeds")
    app.register_blueprint(search_bp, url_prefix="/search")
    app.register_blueprint(wagtail_bp)

    return app
