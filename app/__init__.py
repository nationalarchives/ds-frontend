import re

from app.lib import cache, image_details, page_details
from config import Config
from flask import Flask
from jinja2 import ChoiceLoader, PackageLoader
from markdown import markdown


def create_app(config_class=Config):
    app = Flask(__name__, static_url_path="/static")
    app.config.from_object(config_class)

    cache.init_app(app)

    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True
    app.jinja_loader = ChoiceLoader(
        [
            PackageLoader("app"),
            PackageLoader("tna_frontend_jinja"),
        ]
    )

    @app.template_filter("tna_html")
    def tna_html_filter(s):
        return s.replace("<ul>", '<ul class="tna-ul">').replace(
            "<ol>", '<ol class="tna-ol">'
        )

    @app.template_filter("slugify")
    def slugify(s):
        s = s.lower().strip()
        s = re.sub(r"[^\w\s-]", "", s)
        s = re.sub(r"[\s_-]+", "-", s)
        s = re.sub(r"^-+|-+$", "", s)
        return s

    @app.context_processor
    def cms_processor():
        def get_wagtail_image(image_id):
            image_data = image_details(image_id)
            return image_data

        def get_wagtail_page(page_id):
            page_data = page_details(page_id)
            return page_data

        return dict(
            get_wagtail_image=get_wagtail_image,
            get_wagtail_page=get_wagtail_page,
        )

    from .explore import bp as explore_bp
    from .main import bp as site_bp
    from .wagtail import bp as wagtail_bp

    app.register_blueprint(site_bp)
    app.register_blueprint(explore_bp, url_prefix="/explore-the-collection")
    app.register_blueprint(wagtail_bp)

    return app
