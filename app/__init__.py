from config import Config
from flask import Flask

# from flask_caching import Cache
from markdown import markdown


def create_app(config_class=Config):
    app = Flask(__name__, static_url_path="/static")
    app.config.from_object(config_class)
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True
    # cache = Cache(app)

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

    from app.site import bp as site_bp

    app.register_blueprint(site_bp)

    return app
