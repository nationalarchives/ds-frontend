import requests
from app.lib import BaseAPI
from app.lib.xml import strip_scope_and_content
from config import Config
from pyquery import PyQuery


class BaseCatalogueAPI(BaseAPI):
    def __init__(self):
        super().__init__(Config().ROSETTA_API_URL)


class RecordsAPI(BaseCatalogueAPI):
    api_path = "/fetch/"

    def set_record_id(self, value):
        self.add_parameter("id", value)

    def parse_response(self, response):
        try:
            json_response = response.json()
            if json_response["found"]:
                return json_response
            raise Exception("Resource not found")
        except requests.exceptions.JSONDecodeError:
            raise ConnectionError("API provided non-JSON response")


class RecordParser:
    def __init__(self, rosetta_data):
        self.data = rosetta_data
        self.source = self.data["metadata"][0]["_source"]

    def all(self):
        return (
            self.names()
            | self.date()
            | self.places()
            | self.gender()
            | self.contact_info()
            | self.descriptions()
            | self.identifiers()
            | self.agents()
        )

    def names(self):
        names = {}
        if "name" in self.source:
            name_data = next(
                (
                    item
                    for item in self.source["name"]
                    if "primary" in item and item["primary"]
                ),
                None,
            )
            if name_data:
                if "last" in name_data:
                    names["Surname"] = name_data["last"]
                if "first" in name_data:
                    names["Forenames"] = " ".join(name_data["first"])
                if "title" in name_data:
                    names["Title"] = name_data["title"]
                if "title_prefix" in name_data:
                    names["Pretitle"] = name_data["title_prefix"]
            aka = next(
                (
                    item["value"]
                    for item in self.source["name"]
                    if "type" in item and item["type"] == "also known as"
                ),
                None,
            )
            if aka:
                names["Alternative name(s)"] = aka
        return names

    def date(self):
        date = {}
        source = self.source
        if "birth" in source or "death" in source:
            date_from = (
                source["birth"]["date"]["value"] if "birth" in source else ""
            )
            date_to = (
                source["death"]["date"]["value"] if "death" in source else ""
            )
            date["Date"] = f"{date_from}&ndash;{date_to}"
        elif "start" in source or "end" in source:
            date_from = (
                source["start"]["date"][0]["value"] if "start" in source else ""
            )
            date_to = (
                source["end"]["date"][0]["value"] if "end" in source else ""
            )
            date["Date"] = f"{date_from}&ndash;{date_to}"
        return date

    def places(self):
        places = {}
        if "place" in self.source:
            places["Places"] = "<br>".join(
                # place["name"][0]["value"] for place in self.source["place"]  # Fine for people, not for archives
                []
            )
        return places

    def gender(self):
        gender = {}
        if "gender" in self.source:
            gender["Gender"] = (
                "Male"
                if self.source["gender"] == "M"
                else "Female"
                if self.source["gender"] == "F"
                else self.source["gender"]
            )
        return gender

    def contact_info(self):
        contact_info = {}
        if "description" in self.source:
            ephemera = next(
                (
                    item["ephemera"]["value"]
                    for item in self.source["description"]
                    if "primary" in item and item["primary"]
                ),
                None,
            )
            if ephemera:
                document = PyQuery(ephemera)
                contact_info["address_line1"] = document("addressline1").text()
                contact_info["address_town"] = document("addresstown").text()
                contact_info["postcode"] = document("postcode").text()
                contact_info["address_country"] = document(
                    "addresscountry"
                ).text()
                contact_info["map_url"] = document("mapurl").text()
                contact_info["url"] = document("url").text()
                contact_info["telephone"] = document("telephone").text()
                contact_info["fax"] = document("fax").text()
                contact_info["email"] = document("email").text()
                contact_info["corresp_addr"] = document("correspaddr").text()
                contact_info["contact_job_title"] = document("jobtitle").text()
                contact_info["contact_title"] = document("title").text()
                contact_info["contact_first_name"] = document(
                    "firstname"
                ).text()
                contact_info["contact_last_name"] = document("lastname").text()
        return contact_info

    def descriptions(self):
        descriptions = {}
        if "description" in self.source:
            description = next(
                (
                    item["ephemera"]["value"]
                    for item in self.source["description"]
                    if "primary" in item and item["primary"]
                ),
                None,
            )
            if description:
                descriptions["Description"] = description
                document = PyQuery(description)
                for tag in ("address", "function"):
                    if doc_value := document(tag).text():
                        descriptions["Description"] = doc_value

            functions = next(
                (
                    item["value"]
                    for item in self.source["description"]
                    if "type" in item
                    and item["type"] == "functions, occupations and activities"
                ),
                None,
            )
            if functions:
                descriptions[
                    "Functions, occupations and activities"
                ] = functions
                document = PyQuery(functions)
                for tag in ("foa", "function"):
                    if doc_value := document(tag).text():
                        descriptions[
                            "Functions, occupations and activities"
                        ] = doc_value

            history = next(
                (
                    item["value"]
                    for item in self.source["description"]
                    if "type" in item and item["type"] == "history"
                ),
                None,
            )
            if history:
                descriptions["History"] = history

            biography = next(
                (
                    item
                    for item in self.source["description"]
                    if "type" in item and item["type"] == "biography"
                ),
                None,
            )
            if biography:
                url = biography["url"]
                text = biography["value"]
                url = f'<a href="{url}">{text}</a>'
                descriptions["Biography"] = url
        return descriptions

    def identifiers(self):
        identifiers = {}
        if "identifier" in self.source:
            primary_identifier = next(
                (
                    item["value"]
                    for item in self.source["identifier"]
                    if "type" in item
                    and item["type"] == "name authority reference"
                ),
                None,
            )
            former_identifier = next(
                (
                    item["value"]
                    for item in self.source["identifier"]
                    if "type" in item
                    and item["type"] == "former name authority reference"
                ),
                None,
            )
            identifiers["Name authority identifier"] = (
                f"{primary_identifier} (Former ISAAR ref: {former_identifier})"
                if former_identifier
                else primary_identifier
            )
        return identifiers

    def agents(self):
        agents = {}
        if "agent" in self.source:
            print("here")
            businesses = [
                agent
                for agent in self.source["agent"]
                if agent["identifier"][0]["value"] == "B"
            ]
            print(len(businesses))
            if len(businesses):
                print("here2")
                agents["Businesses"] = businesses
            diaries = [
                agent
                for agent in self.source["agent"]
                if agent["identifier"][0]["value"] == "D"
            ]
            if len(diaries):
                agents["Diaries"] = diaries
            families = [
                agent
                for agent in self.source["agent"]
                if agent["identifier"][0]["value"] == "F"
            ]
            if len(families):
                agents["Families"] = families
            organisations = [
                agent
                for agent in self.source["agent"]
                if agent["identifier"][0]["value"] == "O"
            ]
            if len(organisations):
                agents["Organisations"] = organisations
            persons = [
                agent
                for agent in self.source["agent"]
                if agent["identifier"][0]["value"] == "P"
            ]
            if len(persons):
                agents["Persons"] = persons
        return agents
