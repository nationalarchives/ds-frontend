import logging

import sentry_sdk
from app.lib.cache import cache
from app.lib.context_processor import (
    cookie_preference,
    display_phase_banner,
    is_date_today_or_future,
    is_today_in_date_range,
    now_iso_8601,
    now_iso_8601_no_time,
    now_rfc_822,
    pretty_date_range,
    pretty_datetime_range,
    pretty_price_range,
)
from app.lib.talisman import talisman
from app.lib.template_filters import (
    currency,
    file_type_icon,
    get_url_domain,
    headings_list,
    multiline_address_to_single_line,
    number_to_text,
    parse_json,
    pretty_date,
    pretty_date_with_day,
    pretty_date_with_day_and_time,
    pretty_date_with_time,
    pretty_price,
    qs_active,
    qs_remove,
    qs_toggler,
    qs_update,
    rfc_822_format,
    seconds_to_iso_8601_duration,
    seconds_to_time,
    sidebar_items_from_wagtail_body,
    slugify,
    tna_html,
    unslugify,
    wagtail_streamfield_contains_media,
    wagtail_table_parser,
)
from flask import Flask, request
from jinja2 import ChoiceLoader, PackageLoader
from sentry_sdk.types import Event, Hint


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

    cache.init_app(
        app,
        config={
            "CACHE_TYPE": app.config.get("CACHE_TYPE"),
            "CACHE_DEFAULT_TIMEOUT": app.config.get("CACHE_DEFAULT_TIMEOUT"),
            "CACHE_IGNORE_ERRORS": app.config.get("CACHE_IGNORE_ERRORS"),
            "CACHE_DIR": app.config.get("CACHE_DIR"),
            "CACHE_REDIS_URL": app.config.get("CACHE_REDIS_URL"),
        },
    )

    csp_self = "'self'"
    csp_none = "'none'"
    talisman.init_app(
        app,
        content_security_policy={
            "default-src": csp_self,
            "base-uri": csp_none,
            "object-src": csp_none,
            **(
                {"img-src": app.config.get("CSP_IMG_SRC")}
                if app.config.get("CSP_IMG_SRC") != csp_self
                else {}
            ),
            **(
                {"script-src": app.config.get("CSP_SCRIPT_SRC")}
                if app.config.get("CSP_SCRIPT_SRC") != csp_self
                else {}
            ),
            **(
                {"script-src-elem": app.config.get("CSP_SCRIPT_SRC_ELEM")}
                if app.config.get("CSP_SCRIPT_SRC_ELEM") != csp_self
                else {}
            ),
            **(
                {"style-src": app.config.get("CSP_STYLE_SRC")}
                if app.config.get("CSP_STYLE_SRC") != csp_self
                else {}
            ),
            **(
                {"font-src": app.config.get("CSP_FONT_SRC")}
                if app.config.get("CSP_FONT_SRC") != csp_self
                else {}
            ),
            **(
                {"connect-src": app.config.get("CSP_CONNECT_SRC")}
                if app.config.get("CSP_CONNECT_SRC") != csp_self
                else {}
            ),
            **(
                {"media-src": app.config.get("CSP_MEDIA_SRC")}
                if app.config.get("CSP_MEDIA_SRC") != csp_self
                else {}
            ),
            **(
                {"worker-src": app.config.get("CSP_WORKER_SRC")}
                if app.config.get("CSP_WORKER_SRC") != csp_self
                else {}
            ),
            **(
                {"frame-src": app.config.get("CSP_FRAME_SRC")}
                if app.config.get("CSP_FRAME_SRC") != csp_self
                else {}
            ),
            **(
                {"frame-ancestors": app.config.get("CSP_FRAME_ANCESTORS")}
                if app.config.get("CSP_FRAME_ANCESTORS") != csp_self
                else {}
            ),
        },
        feature_policy={
            "camera": csp_none,
            "fullscreen": app.config.get("CSP_FEATURE_FULLSCREEN") or csp_self,
            "geolocation": csp_none,
            "microphone": csp_none,
            "screen-wake-lock": csp_none,
            "picture-in-picture": app.config.get("CSP_FEATURE_PICTURE_IN_PICTURE")
            or csp_self,
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
    app.add_template_filter(get_url_domain)
    app.add_template_filter(headings_list)
    app.add_template_filter(number_to_text)
    app.add_template_filter(parse_json)
    app.add_template_filter(pretty_date)
    app.add_template_filter(pretty_date_with_day)
    app.add_template_filter(pretty_date_with_time)
    app.add_template_filter(pretty_date_with_day_and_time)
    app.add_template_filter(multiline_address_to_single_line)
    app.add_template_filter(pretty_price)
    app.add_template_filter(rfc_822_format)
    app.add_template_filter(seconds_to_iso_8601_duration)
    app.add_template_filter(seconds_to_time)
    app.add_template_filter(sidebar_items_from_wagtail_body)
    app.add_template_filter(slugify)
    app.add_template_filter(tna_html)
    app.add_template_filter(unslugify)
    app.add_template_filter(wagtail_streamfield_contains_media)
    app.add_template_filter(wagtail_table_parser)

    @app.context_processor
    def context_processor():
        return dict(
            cookie_preference=cookie_preference,
            display_phase_banner=display_phase_banner,
            now_iso_8601=now_iso_8601,
            now_iso_8601_no_time=now_iso_8601_no_time,
            now_rfc_822=now_rfc_822,
            pretty_date_range=pretty_date_range,
            pretty_datetime_range=pretty_datetime_range,
            pretty_price_range=pretty_price_range,
            is_today_in_date_range=is_today_in_date_range,
            is_date_today_or_future=is_date_today_or_future,
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
                "TNA_FRONTEND_VERSION": app.config.get("TNA_FRONTEND_VERSION"),
                "BUILD_VERSION": app.config.get("BUILD_VERSION"),
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

    from .catalogue import bp as catalogue_bp
    from .feeds import bp as feeds_bp
    from .main import bp as site_bp
    from .search import bp as search_bp
    from .site_search import bp as site_search_bp
    from .sitemaps import bp as sitemaps_bp
    from .wagtail import bp as wagtail_bp

    app.register_blueprint(site_bp)
    app.register_blueprint(feeds_bp)
    app.register_blueprint(sitemaps_bp)
    app.register_blueprint(site_search_bp, url_prefix="/search/site")
    app.register_blueprint(search_bp, url_prefix="/search")
    app.register_blueprint(catalogue_bp, url_prefix="/catalogue")
    app.register_blueprint(wagtail_bp)

    return app
