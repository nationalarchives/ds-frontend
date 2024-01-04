import json

import requests
from config import Config
from flask import current_app


class BaseSearchAPI:
    api_url = Config().SEARCH_API_URL
    api_path = "/"
    params = {}

    def query(self, value):
        self.add_parameter("q", value)

    def add_parameter(self, key, value):
        self.params[key] = value

    def build_query_string(self):
        return (
            "?"
            + "&".join(
                [
                    "=".join((key, str(value)))
                    for key, value in self.params.items()
                ]
            )
            if len(self.params)
            else ""
        )

    def get_results(self, page=None):
        if page:
            self.add_parameter("page", page)
        url = f"{self.api_url}{self.api_path}{self.build_query_string()}"
        response = requests.get(url)
        if response.status_code == 404:
            raise Exception("Resource not found")
        if response.status_code == requests.codes.ok:
            return self.parse_response(response)
        raise ConnectionError("Request to API failed")

    def parse_response(self, response):
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            raise ConnectionError("API provided non-JSON response")


class RecordsAPI(BaseSearchAPI):
    api_path = "/records/"


class ArticlesAPI(BaseSearchAPI):
    api_path = "/articles/"

    def parse_response(self, response):
        try:
            if Config().ENVIRONMENT == "develop":
                text = response.text
                text = text.replace(
                    "https://main-bvxea6i-ncoml7u56y47e.uk-1.platformsh.site/",
                    "http://localhost:65535/",
                ).replace(
                    "https://develop-sr3snxi-rasrzs7pi6sd4.uk-1.platformsh.site/",
                    "http://localhost:65535/",
                )
                return json.loads(text)
            return response.json()
        except requests.exceptions.JSONDecodeError:
            current_app.logger.error("API provided non-JSON response")
            raise ConnectionError("API provided non-JSON response")


class ArticleFiltersAPI(BaseSearchAPI):
    api_path = "/articles/filters/"
