import json

import requests
from app.lib import BaseAPI
from config import Config
from flask import current_app


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
