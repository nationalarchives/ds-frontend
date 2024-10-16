import requests
from flask import current_app


class ApiResourceNotFound(Exception):
    pass


class JSONAPIClient:
    api_url = ""
    params = {}

    def __init__(self, api_url):
        self.api_url = api_url

    def add_parameter(self, key, value):
        self.params[key] = value

    def add_parameters(self, params):
        self.params = self.params | params

    def get(self, path="/"):
        url = f"{self.api_url}/{path.lstrip(" / ")}"
        try:
            response = requests.get(url, params=self.params)
        except ConnectionError:
            current_app.logger.error(
                f"JSON API connection error for: {response.url}"
            )
            raise Exception("A connection error occured with the JSON API")
        if response.status_code == requests.codes.ok:
            current_app.logger.debug(
                f"JSON API endpoint requested: {response.url}"
            )
            try:
                return response.json()
            except requests.exceptions.JSONDecodeError:
                current_app.logger.error("JSON API provided non-JSON response")
                raise ConnectionError("JSON API provided non-JSON response")
        if response.status_code == 403:
            current_app.logger.warning(f"Forbidden: {response.url}")
            raise ConnectionError("Forbidden")
        if response.status_code == 404:
            current_app.logger.warning(f"Resource not found: {response.url}")
            raise ApiResourceNotFound("Resource not found")
        current_app.logger.error(
            f"JSON API responded with {response.status_code} status for {response.url}"
        )
        raise ConnectionError("Request to API failed")
