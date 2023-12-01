from flask import Flask
from jinja2 import ChoiceLoader, PackageLoader
from markdown import markdown

from app.lib import cache, image_details
from config import Config


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

    @app.template_filter()
    def md(md):
        return (
            markdown(md)
            .replace("<h1>", '<h1 class="tna-heading-xl">')
            .replace("<h2>", '<h2 class="tna-heading-l">')
            .replace("<h3>", '<h3 class="tna-heading-m">')
            .replace("<p>", '<p class="tna-p">')
            .replace("<ul>", '<ul class="tna-ul">')
            .replace("<ol>", '<ol class="tna-ol">')
            .replace("<blockquote>", '<blockquote class="tna-blockquote">')
        )

    @app.context_processor
    def cms_processor():
        def get_wagtail_image(image_id):
            image_data = image_details(image_id)
            return image_data

        return dict(get_wagtail_image=get_wagtail_image)

    from .explore import bp as explore_bp
    from .main import bp as site_bp
    from .wagtail import bp as wagtail_bp

    app.register_blueprint(site_bp)
    app.register_blueprint(explore_bp, url_prefix="/explore-the-collection")
    app.register_blueprint(wagtail_bp)

    return app
