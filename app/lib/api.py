from flask import current_app
from requests import JSONDecodeError, Timeout, TooManyRedirects, codes, get, post


class ResourceNotFound(Exception):
    pass


class ResourceForbidden(Exception):
    pass


class JSONAPIClient:
    api_url = ""
    headers = {
        "Cache-Control": "no-cache",
        "Accept": "application/json",
    }
    params = {}

    def __init__(self, api_url, params={}):
        self.api_url = api_url
        self.params = params

    def add_parameter(self, key, value):
        self.params[key] = value

    def add_parameters(self, params):
        self.params = self.params | params

    def add_header(self, key, value):
        self.headers[key] = value

    def add_headers(self, headers):
        self.headers = self.headers | headers

    def send(self, method, path="/", data={}):
        url = f"{self.api_url}/{path.lstrip('/')}"
        try:
            if method == "GET":
                response = get(
                    url,
                    params=self.params,
                    headers=self.headers,
                )
            elif method == "POST":
                response = post(
                    url,
                    headers=self.headers,
                    json=data,
                )
            else:
                raise Exception("Unsupported method")
        except ConnectionError:
            current_app.logger.error("JSON API connection error")
            raise Exception("A connection error occured")
        except Timeout:
            current_app.logger.error("JSON API timeout")
            raise Exception("The request timed out")
        except TooManyRedirects:
            current_app.logger.error("JSON API had too many redirects")
            raise Exception("Too many redirects")
        except Exception as e:
            current_app.logger.error(f"Unknown JSON API exception: {e}")
            raise Exception(e)
        return self.process_response(response)

    def get(self, path="/"):
        return self.send("GET", path)

    def post(self, path="/", data={}):
        return self.send("POST", path, data)

    def process_response(self, response):
        current_app.logger.debug(response.url)
        if response.status_code in [codes.ok, codes.created]:
            try:
                return response.json()
            except JSONDecodeError:
                current_app.logger.error("JSON API provided non-JSON response")
                raise Exception("Non-JSON response provided")
        if response.status_code == 400:
            current_app.logger.error(f"Bad request: {response.url}")
            raise Exception("Bad request")
        if response.status_code == 403:
            current_app.logger.warning("Forbidden")
            raise ResourceForbidden("Forbidden")
        if response.status_code == 404:
            current_app.logger.warning("Resource not found")
            raise ResourceNotFound("Resource not found")
        current_app.logger.error(f"JSON API responded with {response.status_code}")
        raise Exception("Request failed")
