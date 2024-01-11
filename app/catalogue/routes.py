import urllib.parse

from app.catalogue import bp
from app.lib import cache, cache_key_prefix
from flask import current_app, render_template

from .api import RecordsAPI


@bp.route("/id/<id>")
@cache.cached(key_prefix=cache_key_prefix)
def record(id):
    records_api = RecordsAPI()
    records_api.set_record_id(id)
    record_data = records_api.get_results()
    data = record_data["metadata"][0]["detail"]["@template"]["details"]
    if data["type"] == "record":
        return render_template("catalogue/record.html", id=id, data=data)
    if data["type"] == "archive":
        return render_template("catalogue/archive.html", id=id, data=data)
    current_app.logger.error(f"Template for {data['type']} not handled")
    return render_template("errors/page-not-found.html"), 404
