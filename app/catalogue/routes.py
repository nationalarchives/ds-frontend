from app.catalogue import bp
from app.lib import cache, cache_key_prefix
from flask import current_app, render_template

from .api import RecordParser, RecordsAPI


@bp.route("/id/<id>/")
@cache.cached(key_prefix=cache_key_prefix)
def info(id):
    records_api = RecordsAPI()
    records_api.set_record_id(id)
    records_api.add_parameter("includeSource", True)
    record_data = records_api.get_results()
    type = record_data["metadata"][0]["_source"]["@datatype"]["base"]
    if type == "record":
        return render_record(id, record_data)
    if type == "archive":
        return render_archive(id, record_data)
    if type == "agent":
        return render_agent(id, record_data)

    current_app.logger.error(f"Template for {type} not handled")
    return render_template("errors/page-not-found.html"), 404


def render_record(id, record_data):
    data = record_data["metadata"][0]["detail"]["@template"]["details"]
    return render_template("catalogue/record.html", id=id, data=data)


def render_archive(id, record_data):
    data = record_data["metadata"][0]["detail"]["@template"]["details"]
    source = record_data["metadata"][0]["_source"]
    record = RecordParser(record_data)
    manifestations = (
        source["manifestations"] if "manifestations" in source else []
    )
    return render_template(
        "catalogue/archive.html",
        id=id,
        data=data,
        places=record.places(),
        contact_info=record.contact_info(),
        agents=record.agents(),
        descriptions=record.descriptions(),
        manifestations=manifestations,
    )


def render_agent(id, record_data):
    record = RecordParser(record_data)
    data = record_data["metadata"][0]["detail"]["@template"]["details"]
    details = record.all()
    return render_template(
        "catalogue/agent.html", id=id, data=data, details=details
    )
