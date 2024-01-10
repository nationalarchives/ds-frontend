import urllib.parse

from app.lib import cache, cache_key_prefix
from app.catalogue import bp
from flask import render_template


@bp.route("/id/<string:id>")
@cache.cached(key_prefix=cache_key_prefix)
def record(id):
    return render_template(
        "catalogue/record.html",
        id=id
    )
