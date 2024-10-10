import logging

import sentry_sdk
from app.lib import cache
from app.lib.context_processor import (
    cookie_preference,
    now_iso_8601,
    pretty_date_range,
)
from app.lib.template_filters import (
    get_url_domain,
    headings_list,
    parse_json,
    pretty_date,
    seconds_to_time,
    sidebar_items_from_wagtail_body,
    slugify,
    tna_html,
    wagtail_streamfield_contains_media,
    wagtail_table_parser,
)
from flask import Flask
from flask_talisman import Talisman
from jinja2 import ChoiceLoader, PackageLoader


def create_app(config_class):
    app = Flask(__name__, static_url_path="/static")
    app.config.from_object(config_class)

    if app.config.get("SENTRY_DSN"):
        sentry_sdk.init(
            dsn=app.config.get("SENTRY_DSN"),
            environment=app.config.get("ENVIRONMENT"),
            release=(
                f"ds-frontend@{app.config.get('BUILD_VERSION')}"
                if app.config.get("BUILD_VERSION")
                else ""
            ),
            sample_rate=app.config.get("SENTRY_SAMPLE_RATE"),
            traces_sample_rate=app.config.get("SENTRY_SAMPLE_RATE"),
            profiles_sample_rate=app.config.get("SENTRY_SAMPLE_RATE"),
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
        },
    )

    csp_self = "'self'"
    csp_none = "'none'"
    Talisman(
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
        },
        feature_policy={
            "camera": csp_none,
            "fullscreen": app.config.get("CSP_FEATURE_FULLSCREEN") or csp_self,
            "geolocation": csp_none,
            "microphone": csp_none,
            "screen-wake-lock": csp_none,
            "picture-in-picture": app.config.get(
                "CSP_FEATURE_PICTURE_IN_PICTURE"
            )
            or csp_self,
        },
        force_https=app.config.get("FORCE_HTTPS"),
        frame_options="ALLOW-FROM",
        frame_options_allow_from=app.config.get("FRAME_DOMAIN_ALLOW"),
    )

    @app.after_request
    def apply_extra_headers(response):
        response.headers["X-Permitted-Cross-Domain-Policies"] = "none"
        response.headers["Cross-Origin-Embedder-Policy"] = "unsafe-none"
        response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
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

    app.add_template_filter(get_url_domain)
    app.add_template_filter(headings_list)
    app.add_template_filter(parse_json)
    app.add_template_filter(pretty_date)
    app.add_template_filter(seconds_to_time)
    app.add_template_filter(sidebar_items_from_wagtail_body)
    app.add_template_filter(slugify)
    app.add_template_filter(tna_html)
    app.add_template_filter(wagtail_streamfield_contains_media)
    app.add_template_filter(wagtail_table_parser)

    @app.context_processor
    def context_processor():
        return dict(
            cookie_preference=cookie_preference,
            now_iso_8601=now_iso_8601,
            pretty_date_range=pretty_date_range,
            app_config={
                "ENVIRONMENT": app.config.get("ENVIRONMENT"),
                "TNA_FRONTEND_VERSION": app.config.get("TNA_FRONTEND_VERSION"),
                "BUILD_VERSION": app.config.get("BUILD_VERSION"),
                "COOKIE_DOMAIN": app.config.get("COOKIE_DOMAIN"),
                "GA4_ID": app.config.get("GA4_ID"),
                "SENTRY_JS_ID": app.config.get("SENTRY_JS_ID"),
                "SENTRY_SAMPLE_RATE": app.config.get("SENTRY_SAMPLE_RATE"),
            },
            feature={
                "PHASE_BANNER": app.config.get("FEATURE_PHASE_BANNER"),
            },
        )

    from .main import bp as site_bp
    from .search import bp as search_bp
    from .wagtail import bp as wagtail_bp

    app.register_blueprint(site_bp)
    app.register_blueprint(search_bp, url_prefix="/search")
    app.register_blueprint(wagtail_bp)

    return app
