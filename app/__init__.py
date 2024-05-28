import logging

from app.lib import cache
from app.lib.context_processor import (
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
    to_bool,
    url_encode,
)
from config import Config, templates_config
from flask import Flask
from flask_talisman import Talisman
from jinja2 import ChoiceLoader, PackageLoader


def create_app(config_class=Config):
    app = Flask(__name__, static_url_path="/static")
    app.config.from_object(config_class)

    gunicorn_error_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers.extend(gunicorn_error_logger.handlers)
    app.logger.setLevel(gunicorn_error_logger.level)

    cache.init_app(app)

    SELF = "'self'"
    Talisman(
        app,
        content_security_policy={
            "default-src": SELF,
            "img-src": [
                SELF,
                Config().DOMAIN,
                Config().MEDIA_DOMAIN,
                "https://*.google-analytics.com",
                "https://*.googletagmanager.com",
                (
                    "https://googletagmanager.com"
                    if Config().ENVIRONMENT != "develop"
                    else "http://googletagmanager.com"
                ),
                "https://ssl.gstatic.com",
                "https://www.gstatic.com",
            ],
            "script-src": [
                SELF,
                "https://*.googletagmanager.com",
                (
                    "https://googletagmanager.com"
                    if Config().ENVIRONMENT != "develop"
                    else "http://googletagmanager.com"
                ),
                (
                    "https://tagmanager.google.com"
                    if Config().ENVIRONMENT != "develop"
                    else "http://tagmanager.google.com"
                ),
            ],
            "style-src": [
                SELF,
                "https://fonts.googleapis.com",
                "https://p.typekit.net",
                "https://use.typekit.net",
                (
                    "https://googletagmanager.com"
                    if Config().ENVIRONMENT != "develop"
                    else "http://googletagmanager.com"
                ),
                (
                    "https://www.googletagmanager.com"
                    if Config().ENVIRONMENT != "develop"
                    else "http://www.googletagmanager.com"
                ),
                (
                    "https://tagmanager.google.com"
                    if Config().ENVIRONMENT != "develop"
                    else "http://tagmanager.google.com"
                ),
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
                Config().MEDIA_DOMAIN,
            ],
        },
        feature_policy={
            "camera": "'none'",
            "fullscreen": "'self'",
            "geolocation": "'none'",
            "microphone": "'none'",
            "screen-wake-lock": "'none'",
        },
        force_https=Config().ENVIRONMENT != "develop",
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
    app.add_template_filter(to_bool)

    @app.context_processor
    def context_processor():
        return dict(
            merge_dict=merge_dict,
            merge_dict_if=merge_dict_if,
            now_iso_8601=now_iso_8601,
            pretty_date_range=pretty_date_range,
            config=templates_config,
        )

    from .catalogue import bp as catalogue_bp
    from .main import bp as site_bp
    from .search import bp as search_bp
    from .wagtail import bp as wagtail_bp

    app.register_blueprint(site_bp)
    app.register_blueprint(search_bp, url_prefix="/search")
    app.register_blueprint(catalogue_bp, url_prefix="/catalogue")
    app.register_blueprint(wagtail_bp)

    return app
