from flask import current_app
from requests import JSONDecodeError, Timeout, TooManyRedirects, codes, get


class ResourceNotFoundError(Exception):
    pass


class ResourceForbiddenError(Exception):
    pass


class JSONAPIClient:
    def __init__(self, api_url, default_headers=None, default_params=None):
        self.api_url = api_url
        self.headers = {
            "Cache-Control": "no-cache",
            "Accept": "application/json",
        }
        self.params = {}
        if default_headers is not None:
            self.headers = self.headers | default_headers
        if default_params is not None:
            self.params = self.params | default_params

    def add_parameter(self, key, value):
        self.params[key] = value

    def add_parameters(self, params):
        self.params = self.params | params

    def add_header(self, key, value):
        self.headers[key] = value

    def add_headers(self, headers):
        self.headers = self.headers | headers

    def get(self, path="/"):
        url = f"{self.api_url}/{path.lstrip('/')}"
        try:
            response = get(
                url,
                params=self.params,
                headers=self.headers,
            )
        except ConnectionError as e:
            current_app.logger.exception("JSON API connection error")
            raise Exception("A connection error occured") from e
        except Timeout as e:
            current_app.logger.exception("JSON API timeout")
            raise Exception("The request timed out") from e
        except TooManyRedirects as e:
            current_app.logger.exception("JSON API had too many redirects")
            raise Exception("Too many redirects") from e
        except Exception as e:
            current_app.logger.exception("Unknown JSON API exception")
            raise Exception(e) from e
        current_app.logger.debug(response.url)
        if response.status_code == codes.ok:
            try:
                return response.json()
            except JSONDecodeError as e:
                current_app.logger.exception("JSON API provided non-JSON response")
                raise Exception("Non-JSON response provided") from e
        if response.status_code == 400:
            current_app.logger.exception(f"Bad request: {response.url}")
            raise Exception("Bad request")
        if response.status_code == 403:
            current_app.logger.warning("Forbidden")
            raise ResourceForbiddenError("Forbidden")
        if response.status_code == 404:
            current_app.logger.warning("Resource not found")
            raise ResourceNotFoundError("Resource not found")
        current_app.logger.exception(f"JSON API responded with {response.status_code}")
        raise Exception("Request failed")
