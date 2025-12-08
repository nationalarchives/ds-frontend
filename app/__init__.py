import logging

import sentry_sdk
from app.lib.context_processor import (
    cookie_preference,
    display_phase_banner,
    now_iso_8601,
    now_iso_8601_date,
    now_rfc_822,
)
from app.lib.query import (
    qs_active,
    qs_remove,
    qs_toggler,
    qs_update,
)
from app.lib.talisman import talisman
from app.lib.template_filters import (
    file_type_icon,
    get_url_domain,
    headings_list,
    multiline_address_to_single_line,
    number_to_text,
    parse_json,
    pretty_date_with_day,
    pretty_date_with_day_and_time,
    pretty_date_with_time,
    sidebar_items_from_wagtail_streamfield,
    slugify,
    tna_html,
    truncate,
    unslugify,
    url_encode,
    wagtail_streamfield_contains_media,
    wagtail_table_parser,
)
from flask import Flask, request
from jinja2 import ChoiceLoader, PackageLoader
from sentry_sdk.types import Event, Hint
from tna_utilities.currency import currency, pretty_price, pretty_price_range
from tna_utilities.datetime import (
    is_today_or_future,
    pretty_date,
    pretty_date_range,
    pretty_datetime_range,
    rfc_822_date_format,
    seconds_to_duration,
    seconds_to_iso_8601_duration,
    is_today_in_date_range,get_date_from_string
)


def create_app(config_class):
    app = Flask(__name__, static_url_path="/static")
    app.config.from_object(config_class)

    if app.config.get("SENTRY_DSN"):

        def before_send(event: Event, hint: Hint) -> Event | None:
            # Filter out preview page errors
            if event.get("transaction") == "wagtail.preview_page":
                return None
            return event

        sentry_sdk.init(
            dsn=app.config.get("SENTRY_DSN"),
            environment=app.config.get("ENVIRONMENT_NAME"),
            release=(
                f"ds-frontend@{app.config.get('BUILD_VERSION')}"
                if app.config.get("BUILD_VERSION")
                else ""
            ),
            sample_rate=app.config.get("SENTRY_SAMPLE_RATE"),
            traces_sample_rate=app.config.get("SENTRY_SAMPLE_RATE"),
            profiles_sample_rate=app.config.get("SENTRY_SAMPLE_RATE"),
            before_send=before_send,
        )

    gunicorn_error_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers.extend(gunicorn_error_logger.handlers)
    app.logger.setLevel(gunicorn_error_logger.level or "DEBUG")

    csp_self = "'self'"
    csp_none = "'none'"
    default_csp = csp_self
    csp_rules = {
        key.replace("_", "-"): value
        for key, value in app.config.get_namespace(
            "CSP_", lowercase=True, trim_namespace=True
        ).items()
        if not key.startswith("feature_")
        and not key.startswith("report_")
        and value not in [None, [default_csp]]
    }
    talisman.init_app(
        app,
        content_security_policy={
            "default-src": default_csp,
            "base-uri": csp_none,
            "object-src": csp_none,
        }
        | csp_rules,
        content_security_policy_report_uri=app.config.get("CSP_REPORT_URL", None),
        feature_policy={
            "fullscreen": app.config.get("CSP_FEATURE_FULLSCREEN", csp_self),
            "picture-in-picture": app.config.get(
                "CSP_FEATURE_PICTURE_IN_PICTURE", csp_self
            ),
        },
        force_https=app.config.get("FORCE_HTTPS"),
    )

    @app.after_request
    def apply_extra_headers(response):
        if "X-Permitted-Cross-Domain-Policies" not in response.headers:
            response.headers["X-Permitted-Cross-Domain-Policies"] = "none"
        if "Cross-Origin-Embedder-Policy" not in response.headers:
            response.headers["Cross-Origin-Embedder-Policy"] = "unsafe-none"
        if "Cross-Origin-Opener-Policy" not in response.headers:
            response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
        if "Cross-Origin-Resource-Policy" not in response.headers:
            response.headers["Cross-Origin-Resource-Policy"] = "same-origin"
        return response

    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True
    app.jinja_loader = ChoiceLoader(
        [
            PackageLoader("app"),
            PackageLoader("tna_frontend_jinja"),
        ]
    )

    app.add_template_filter(currency)
    app.add_template_filter(file_type_icon)
    app.add_template_filter(get_date_from_string)
    app.add_template_filter(get_url_domain)
    app.add_template_filter(headings_list)
    app.add_template_filter(is_today_or_future)
    app.add_template_filter(number_to_text)
    app.add_template_filter(parse_json)
    app.add_template_filter(pretty_date)
    app.add_template_filter(pretty_date_with_day)
    app.add_template_filter(pretty_date_with_time)
    app.add_template_filter(pretty_date_with_day_and_time)
    app.add_template_filter(multiline_address_to_single_line)
    app.add_template_filter(pretty_price)
    app.add_template_filter(rfc_822_date_format)
    app.add_template_filter(seconds_to_iso_8601_duration)
    app.add_template_filter(seconds_to_duration)
    app.add_template_filter(sidebar_items_from_wagtail_streamfield)
    app.add_template_filter(slugify)
    app.add_template_filter(tna_html)
    app.add_template_filter(truncate)
    app.add_template_filter(unslugify)
    app.add_template_filter(url_encode)
    app.add_template_filter(wagtail_streamfield_contains_media)
    app.add_template_filter(wagtail_table_parser)

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
            qs_active=lambda filter, by: qs_active(request.args.to_dict(), filter, by),
            qs_toggler=lambda filter, by: qs_toggler(
                request.args.to_dict(), filter, by
            ),
            qs_update=lambda filter, value: qs_update(
                request.args.to_dict(), filter, value
            ),
            qs_remove=lambda filter: qs_remove(request.args.to_dict(), filter),
            app_config={
                "ENVIRONMENT_NAME": app.config.get("ENVIRONMENT_NAME"),
                "CONTAINER_IMAGE": app.config.get("CONTAINER_IMAGE"),
                "BUILD_VERSION": app.config.get("BUILD_VERSION"),
                "TNA_FRONTEND_VERSION": app.config.get("TNA_FRONTEND_VERSION"),
                "COOKIE_DOMAIN": app.config.get("COOKIE_DOMAIN"),
                "GA4_ID": app.config.get("GA4_ID"),
                "SENTRY_JS_ID": app.config.get("SENTRY_JS_ID"),
                "SENTRY_SAMPLE_RATE": app.config.get("SENTRY_SAMPLE_RATE"),
            },
            feature={
                "PHASE_BANNER": app.config.get("FEATURE_PHASE_BANNER"),
                "LOGO_ADORNMENTS_CSS": app.config.get("FEATURE_LOGO_ADORNMENTS_CSS"),
                "LOGO_ADORNMENTS_JS": app.config.get("FEATURE_LOGO_ADORNMENTS_JS"),
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
