import logging

from app.lib import cache
from app.lib.context_processor import (
    cookie_preference,
    merge_dict,
    merge_dict_if,
    now_iso_8601,
    pretty_date_range,
)
from app.lib.template_filters import (
    headings_list,
    iso_date,
    pretty_date,
    pretty_number,
    remove_all_whitespace,
    replace_ext_ref,
    replace_ref,
    slugify,
    tna_html,
    url_encode,
)
from flask import Flask
from flask_talisman import Talisman
from jinja2 import ChoiceLoader, PackageLoader


def create_app(config_class):
    app = Flask(__name__, static_url_path="/static")
    app.config.from_object(config_class)

    gunicorn_error_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers.extend(gunicorn_error_logger.handlers)
    app.logger.setLevel(gunicorn_error_logger.level or "DEBUG")

    cache.init_app(
        app,
        config={
            "CACHE_TYPE": app.config["CACHE_TYPE"],
            "CACHE_DEFAULT_TIMEOUT": app.config["CACHE_DEFAULT_TIMEOUT"],
            "CACHE_IGNORE_ERRORS": app.config["CACHE_IGNORE_ERRORS"],
            "CACHE_DIR": app.config["CACHE_DIR"],
        },
    )

    SELF = "'self'"
    Talisman(
        app,
        content_security_policy={
            "default-src": SELF,
            "base-uri": "'none'",
            "img-src": [
                SELF,
                app.config["DOMAIN"],
                app.config["MEDIA_DOMAIN"],
                "https://*.google-analytics.com",
                "https://*.googletagmanager.com",
                "https://googletagmanager.com",
                # "http://googletagmanager.com",
                "https://ssl.gstatic.com",
                "https://www.gstatic.com",
                "https://www.nationalarchives.gov.uk",
                "https://beta.nationalarchives.gov.uk",
                "https://develop-sr3snxi-rasrzs7pi6sd4.uk-1.platformsh.site",
            ],
            "script-src": [
                SELF,
                "https://*.googletagmanager.com",
                "https://googletagmanager.com",
                # "http://googletagmanager.com",
                "https://tagmanager.google.com",
                # "http://tagmanager.google.com",
            ],
            "style-src": [
                SELF,
                "https://fonts.googleapis.com",
                "https://p.typekit.net",
                "https://use.typekit.net",
                "https://googletagmanager.com",
                # "http://googletagmanager.com",
                "https://www.googletagmanager.com",
                # "http://www.googletagmanager.com",
                "https://tagmanager.google.com",
                # "http://tagmanager.google.com",
            ],
            "font-src": [
                SELF,
                "https://fonts.gstatic.com",
                "https://use.typekit.net",
            ],
            "connect-src": [
                SELF,
                "https://*.google-analytics.com",
                "https://*.analytics.google.com",
                "https://*.googletagmanager.com",
            ],
            "media-src": [
                SELF,
                app.config["MEDIA_DOMAIN"],
            ],
        },
        content_security_policy_nonce_in=["script-src"],
        feature_policy={
            "camera": "'none'",
            "fullscreen": SELF,
            "geolocation": "'none'",
            "microphone": "'none'",
            "screen-wake-lock": "'none'",
        },
        force_https=app.config["FORCE_HTTPS"],
        frame_options="ALLOW-FROM",
        frame_options_allow_from=app.config["WAGTAIL_DOMAIN"],
    )

    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True
    app.jinja_loader = ChoiceLoader(
        [
            PackageLoader("app"),
            PackageLoader("tna_frontend_jinja"),
        ]
    )

    app.add_template_filter(tna_html)
    app.add_template_filter(slugify)
    app.add_template_filter(pretty_date)
    app.add_template_filter(iso_date)
    app.add_template_filter(pretty_number)
    app.add_template_filter(headings_list)
    app.add_template_filter(replace_ref)
    app.add_template_filter(replace_ext_ref)
    app.add_template_filter(remove_all_whitespace)
    app.add_template_filter(url_encode)

    @app.context_processor
    def context_processor():
        return dict(
            merge_dict=merge_dict,
            merge_dict_if=merge_dict_if,
            cookie_preference=cookie_preference,
            now_iso_8601=now_iso_8601,
            pretty_date_range=pretty_date_range,
            config={
                "DOMAIN": app.config["DOMAIN"],
                "BASE_DISCOVERY_URL": app.config["BASE_DISCOVERY_URL"],
                "SEARCH_DISCOVERY_URL": app.config["SEARCH_DISCOVERY_URL"],
                "SEARCH_WEBSITE_URL": app.config["SEARCH_WEBSITE_URL"],
                "ARCHIVE_RECORDS_URL": app.config["ARCHIVE_RECORDS_URL"],
                "GA4_ID": app.config["GA4_ID"],
            },
        )

    from .about import bp as about_bp
    from .catalogue import bp as catalogue_bp
    from .help import bp as help_bp
    from .legal import bp as legal_bp
    from .main import bp as site_bp
    from .search import bp as search_bp
    from .wagtail import bp as wagtail_bp

    app.register_blueprint(site_bp)
    app.register_blueprint(legal_bp, url_prefix="/legal")
    app.register_blueprint(help_bp, url_prefix="/help")
    app.register_blueprint(about_bp, url_prefix="/about")
    app.register_blueprint(search_bp, url_prefix="/search")
    app.register_blueprint(catalogue_bp, url_prefix="/catalogue")
    app.register_blueprint(wagtail_bp)

    return app
