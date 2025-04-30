from app.catalogue import bp

"""
Align paths to routes in https://github.com/nationalarchives/ds-search
"""


message = "Replaced with the contents of ds-search in dev, staging and production"


@bp.route("/")
def index():
    return message


@bp.route("/search/")
def search():
    return message


@bp.route("/id/<id>/")
def catalogue_item(id):
    return message
