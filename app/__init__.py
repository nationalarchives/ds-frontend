import logging

from app.lib import cache
from app.lib.context_processor import (
    get_wagtail_image,
    get_wagtail_media,
    get_wagtail_page,
    now_iso_8601,
)
from app.lib.template_filters import (
    article_supertitle,
    article_type,
    brand_icon_from_url,
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
from jinja2 import ChoiceLoader, PackageLoader


def create_app(config_class=Config):
    app = Flask(__name__, static_url_path="/static")
    app.config.from_object(config_class)

    gunicorn_error_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers.extend(gunicorn_error_logger.handlers)
    app.logger.setLevel(gunicorn_error_logger.level)

    cache.init_app(app)

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
    app.add_template_filter(article_supertitle)
    app.add_template_filter(article_type)
    app.add_template_filter(brand_icon_from_url)
    app.add_template_filter(headings_list)
    app.add_template_filter(replace_ref)
    app.add_template_filter(replace_ext_ref)
    app.add_template_filter(remove_all_whitespace)
    app.add_template_filter(url_encode)
    app.add_template_filter(to_bool)

    @app.context_processor
    def context_processor():
        return dict(
            get_wagtail_image=get_wagtail_image,
            get_wagtail_page=get_wagtail_page,
            get_wagtail_media=get_wagtail_media,
            now_iso_8601=now_iso_8601,
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
