from app.catalogue import bp
from app.lib import cache, cache_key_prefix, parse_cdata
from flask import current_app, render_template

from .api import RecordsAPI


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
    place = source["place"][0]
    agents = source["agent"]
    businesses = [
        agent for agent in agents if agent["identifier"][0]["value"] == "B"
    ]
    diaries = [
        agent for agent in agents if agent["identifier"][0]["value"] == "D"
    ]
    families = [
        agent for agent in agents if agent["identifier"][0]["value"] == "F"
    ]
    organisations = [
        agent for agent in agents if agent["identifier"][0]["value"] == "O"
    ]
    persons = [
        agent for agent in agents if agent["identifier"][0]["value"] == "P"
    ]
    manifestations = source["manifestations"]
    return render_template(
        "catalogue/archive.html",
        id=id,
        data=data,
        place=place,
        businesses=businesses,
        diaries=diaries,
        families=families,
        organisations=organisations,
        persons=persons,
        manifestations=manifestations,
    )


def render_agent(id, record_data):
    data = record_data["metadata"][0]["detail"]["@template"]["details"]
    source = record_data["metadata"][0]["_source"]
    details = {}

    if "name" in source:
        name = next(
            (
                item
                for item in source["name"]
                if "primary" in item and item["primary"]
            ),
            None,
        )
        if name:
            if "last" in name:
                details["Surname"] = name["last"]
            if "first" in name:
                details["Forenames"] = " ".join(name["first"])
            if "title" in name:
                details["Title"] = name["title"]
            if "title_prefix" in name:
                details["Pretitle"] = name["title_prefix"]

        aka = next(
            (
                item["value"]
                for item in source["name"]
                if "type" in item and item["type"] == "also known as"
            ),
            None,
        )
        if aka:
            details["Alternative name(s)"] = aka

    if "birth" in source or "death" in source:
        date_from = (
            source["birth"]["date"]["value"] if "birth" in source else ""
        )
        date_to = source["death"]["date"]["value"] if "death" in source else ""
        details["Date"] = f"{date_from}&ndash;{date_to}"
    elif "start" in source or "end" in source:
        date_from = (
            source["start"]["date"][0]["value"] if "start" in source else ""
        )
        date_to = source["end"]["date"][0]["value"] if "end" in source else ""
        details["Date"] = f"{date_from}&ndash;{date_to}"

    if "place" in source:
        details["Places"] = "<br>".join(
            place["name"][0]["value"] for place in source["place"]
        )

    if "gender" in source:
        details["Gender"] = (
            "Male"
            if source["gender"] == "M"
            else "Female"
            if source["gender"] == "F"
            else source["gender"]
        )

    if "description" in source:
        functions = next(
            (
                item["value"]
                for item in source["description"]
                if "type" in item
                and item["type"] == "functions, occupations and activities"
            ),
            None,
        )
        if functions:
            details["Functions, occupations and activities"] = parse_cdata(
                functions
            )

        history = next(
            (
                item["value"]
                for item in source["description"]
                if "type" in item and item["type"] == "history"
            ),
            None,
        )
        if history:
            details["History"] = history

        biography = next(
            (
                item
                for item in source["description"]
                if "type" in item and item["type"] == "biography"
            ),
            None,
        )
        if biography:
            url = biography["url"]
            text = biography["value"]
            url = f'<a href="{url}">{text}</a>'
            details["Biography"] = url

    if "identifier" in source:
        primary_identifier = next(
            (
                item["value"]
                for item in source["identifier"]
                if "type" in item and item["type"] == "name authority reference"
            ),
            None,
        )
        former_identifier = next(
            (
                item["value"]
                for item in source["identifier"]
                if "type" in item
                and item["type"] == "former name authority reference"
            ),
            None,
        )
        details["Name authority identifier"] = (
            f"{primary_identifier} (Former ISAAR ref: {former_identifier})"
            if former_identifier
            else primary_identifier
        )

    return render_template(
        "catalogue/agent.html", id=id, data=data, details=details
    )
