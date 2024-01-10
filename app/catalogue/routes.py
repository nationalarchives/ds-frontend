import urllib.parse

from app.catalogue import bp
from app.lib import cache, cache_key_prefix
from flask import render_template

from .api import RecordsAPI


@bp.route("/id/<id>")
@cache.cached(key_prefix=cache_key_prefix)
def record(id):
    records_api = RecordsAPI()
    records_api.set_record_id(id)
    data = records_api.get_results()
    return render_template(
        "catalogue/record.html", id=id, data=data["metadata"][0]
    )
