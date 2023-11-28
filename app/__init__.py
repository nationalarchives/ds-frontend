import requests
from app.lib import cache
from config import Config
from flask import Flask
from markdown import markdown


def create_app(config_class=Config):
    app = Flask(__name__, static_url_path="/static")
    app.config.from_object(config_class)
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True
    cache.init_app(app)

    @app.template_filter()
    def md(md):
        return (
            markdown(md)
            .replace("<h1>", '<h1 class="tna-heading tna-heading--xl">')
            .replace("<h2>", '<h2 class="tna-heading tna-heading--l">')
            .replace("<h3>", '<h3 class="tna-heading tna-heading--m">')
            .replace("<p>", '<p class="tna-p">')
            .replace("<ul>", '<ul class="tna-ul">')
            .replace("<ol>", '<ol class="tna-ol">')
            .replace("<blockquote>", '<blockquote class="tna-blockquote">')
        )

    @app.context_processor
    def cms_processor():
        def get_wagtail_image(image_id):
            image_data = requests.get(
                "http://host.docker.internal:8000/api/v2/images/%d/" % image_id
            ).json()
            return image_data

        return dict(get_wagtail_image=get_wagtail_image)

    from .cms import bp as cms_bp
    from .explore import bp as explore_bp
    from .main import bp as site_bp

    app.register_blueprint(site_bp)
    app.register_blueprint(explore_bp, url_prefix="/explore-the-collection")
    app.register_blueprint(cms_bp)

    return app
