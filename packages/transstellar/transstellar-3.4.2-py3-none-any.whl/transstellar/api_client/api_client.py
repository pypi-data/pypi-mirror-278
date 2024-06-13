import http
import json
import logging

import requests

from .errors import ClientError, ServerError, UnauthorizedError


class APIClient:
    token = ""
    headers = {"content-type": "application/json", "accept": "application/json"}
    httpclient_logger = logging.getLogger("http.client")

    def __init__(self, base_url: str, options={}):
        self.base_url = base_url

        if options.get("debug") == True:
            global httpclient_logger

            def httpclient_log(*args):
                self.httpclient_logger.log(logging.DEBUG, " ".join(args))

            # mask the print() built-in in the http.client module to use
            # logging instead
            http.client.print = httpclient_log
            # enable debugging
            http.client.HTTPConnection.debuglevel = 1

    def as_token(self, token):
        self.token = token

        return self

    def get(self, endpoint, params=None, headers=None):

        url = f"{self.base_url}/{endpoint}"

        return self.__get(url, params, headers)

    def post(
        self, endpoint, payload, headers=None, expected_successful_status_code=201
    ):
        url = f"{self.base_url}/{endpoint}"
        return self.__post(url, payload, headers, expected_successful_status_code)

    def patch(
        self, endpoint, payload, headers=None, expected_successful_status_code=200
    ):
        url = f"{self.base_url}/{endpoint}"
        return self.__patch(url, payload, headers, expected_successful_status_code)

    def put(self, endpoint, payload, headers=None, expected_successful_status_code=200):
        url = f"{self.base_url}/{endpoint}"
        return self.__put(url, payload, headers, expected_successful_status_code)

    def delete(self, endpoint, headers=None):
        url = f"{self.base_url}/{endpoint}"

        return self.__delete(url, headers)

    def __get(self, url, params, headers):
        headers = self.__get_headers(headers)

        response = requests.get(url, params=params, headers=headers)

        return self.__handle_response(response)

    def __post(self, url, payload, headers={}, expected_successful_status_code=201):
        headers = self.__get_headers(headers)
        response = requests.post(url, json=payload, headers=headers)

        return self.__handle_response(response, expected_successful_status_code)

    def __patch(self, url, payload, headers={}, expected_successful_status_code=200):
        headers = self.__get_headers(headers)
        response = requests.patch(url, json=payload, headers=headers)

        return self.__handle_response(response, expected_successful_status_code)

    def __put(self, url, payload, headers={}, expected_successful_status_code=200):
        headers = self.__get_headers(headers)
        response = requests.put(url, json=payload, headers=headers)

        return self.__handle_response(response, expected_successful_status_code)

    def __delete(self, url, headers={}):
        headers = self.__get_headers(headers)
        response = requests.delete(url, headers=headers)

        return self.__handle_response(response, expected_successful_status_code=204)

    def __get_headers(self, headers):
        if headers is None:
            headers = {}
        return {**self.headers, **headers, "Authorization": f"Bearer {self.token}"}

    def __handle_response(
        self, response: requests.models.Response, expected_successful_status_code=200
    ):
        status_code = response.status_code
        response_json = None

        if response.text:
            response_json = json.loads(response.text)

        if status_code >= 200 and status_code < 300:
            if status_code != expected_successful_status_code:
                raise Exception(
                    f"Response status code ({status_code}) is not as expected: {expected_successful_status_code}"
                )
            return response_json

        if status_code >= 400 and status_code < 500:
            error_message = response_json.get("message", "Unknown client error")

            if status_code == 400:
                raise ClientError(f"Client error: {error_message}")

            elif status_code == 401:
                raise UnauthorizedError("Unauthorized: Check your credentials")

            else:
                error_message = response_json.get("message", "Unknown client error")
                raise ClientError(f"Client error: HTTP {status_code}. {error_message}")

        if status_code >= 500:
            error_message = response_json.get("message", "Internal Server Error")
            raise ServerError(f"Server error: HTTP {status_code}. {error_message}")
