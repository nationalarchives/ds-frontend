from app.search import bp

"""
Align paths to routes in https://github.com/nationalarchives/ds-sitemap-search
"""


message = (
    "Replaced with the contents of ds-sitemap-search in dev, staging and production"
)


@bp.route("/")
def index():
    return message
