from app.catalogue import bp
from app.lib import cache, cache_key_prefix
from flask import current_app, render_template

from .api import RecordAPI


@bp.route("/id/<id>/")
@cache.cached(key_prefix=cache_key_prefix)
def details(id):
    records_api = RecordAPI(id)
    record_data = records_api.get_results()
    type = record_data["type"]

    if type == "record":
        return render_record(id, record_data)
    if type == "archive":
        return render_archive(id, record_data)
    if type == "creator":
        return render_creator(id, record_data)
    if type == "person":
        return render_person(id, record_data)

    current_app.logger.error(f"Template for {type} not handled")
    return render_template("errors/page-not-found.html"), 404


def render_record(id, record_data):
    return render_template("catalogue/record.html", id=id, data=record_data)


def render_archive(id, record_data):
    address_parts = []
    for address_part in [
        "address_line_1",
        "town",
        "county",
        "country",
        "postcode",
    ]:
        if (
            address_part in record_data["contact_info"]
            and record_data["contact_info"][address_part]
        ):
            address_parts.append(record_data["contact_info"][address_part])
    return render_template(
        "catalogue/archive.html",
        id=id,
        data=record_data,
        address_parts=address_parts,
    )


def render_creator(id, record_data):
    details = {}
    if record_data["date"]:
        details["Date"] = record_data["date"]
    if record_data["places"]:
        details["Places"] = "<br>".join(record_data["places"])
    if record_data["history"]:
        details["History"] = record_data["history"]
    if record_data["identifier"]:
        details["Identifier"] = record_data["identifier"]
    return render_template(
        "catalogue/creator.html", id=id, data=record_data, details=details
    )


def render_person(id, record_data):
    details = {}
    if record_data["name_parts"]:
        if (
            "surname" in record_data["name_parts"]
            and record_data["name_parts"]["surname"]
        ):
            details["Surname"] = record_data["name_parts"]["surname"]
        if (
            "forenames" in record_data["name_parts"]
            and record_data["name_parts"]["forenames"]
        ):
            details["Forenames"] = " ".join(
                record_data["name_parts"]["forenames"]
            )
        if (
            "alternative_names" in record_data["name_parts"]
            and record_data["name_parts"]["alternative_names"]
        ):
            details["Also known as"] = record_data["name_parts"][
                "alternative_names"
            ]
        if (
            "title" in record_data["name_parts"]
            and record_data["name_parts"]["title"]
        ):
            details["Title"] = record_data["name_parts"]["title"]
    if record_data["date"]:
        details["Gender"] = record_data["gender"]
    if record_data["gender"]:
        details["Date"] = record_data["date"]
    if record_data["places"]:
        details["Places"] = "<br>".join(record_data["places"])
    if record_data["history"]:
        details["Functions, occupations and activities"] = record_data[
            "history"
        ]
    if record_data["biography"]:
        details["Biography"] = record_data["biography"]
    if record_data["identifier"]:
        details["Identifier"] = record_data["identifier"]
    return render_template(
        "catalogue/person.html", id=id, data=record_data, details=details
    )
