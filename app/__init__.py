import logging
from datetime import datetime

from app.lib import cache
from app.lib.template_filters import (
    article_supertitle,
    article_type,
    brand_icon_from_url,
    headings_list,
    pretty_date,
    slugify,
    tna_html,
)
from app.wagtail.api import image_details, media_details, page_details
from config import Config
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
    app.add_template_filter(article_supertitle)
    app.add_template_filter(article_type)
    app.add_template_filter(brand_icon_from_url)
    app.add_template_filter(headings_list)

    # app.add_cms_processor(headings_list)

    @app.context_processor
    def cms_processor():
        def get_wagtail_image(image_id):
            image_data = image_details(image_id)
            return image_data

        def get_wagtail_page(page_id):
            page_data = page_details(page_id)
            return page_data

        def get_wagtail_media(media_id):
            media_data = media_details(media_id)
            return media_data

        def now_iso_8601():
            now = datetime.now()
            now_date = now.strftime("%Y-%m-%dT%H:%M:%SZ")
            return now_date

        return dict(
            get_wagtail_image=get_wagtail_image,
            get_wagtail_page=get_wagtail_page,
            get_wagtail_media=get_wagtail_media,
            now_iso_8601=now_iso_8601,
            WAGTAIL_MEDIA_URL=Config().WAGTAIL_MEDIA_URL,
        )

    from .main import bp as site_bp
    from .search import bp as search_bp
    from .wagtail import bp as wagtail_bp

    app.register_blueprint(site_bp)
    app.register_blueprint(search_bp, url_prefix="/search")
    app.register_blueprint(wagtail_bp)

    return app
