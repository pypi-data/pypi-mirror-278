from .api_client import APIClient


class APIResource:
    EMPTY_PATH_PARAMS = {}

    def __init__(self, base_endpoint_template: str, api_client: APIClient):
        self.base_endpoint_template = base_endpoint_template
        self.api_client = api_client

    def find(self, path_params: dict, headers=None):
        endpoint = self.__generate_endpoint(path_params)

        response = self.api_client.get(endpoint=endpoint, headers=headers)

        return response

    def list(self, path_params: dict, params: dict = None, headers=None):
        endpoint = self.__generate_endpoint(path_params)
        response = self.api_client.get(endpoint, params=params, headers=headers)

        return response

    def create(
        self,
        path_params: dict = None,
        payload=None,
        headers=None,
        expected_successful_status_code=201,
    ):
        endpoint = self.__generate_endpoint(path_params)

        response = self.api_client.post(
            endpoint, payload, headers, expected_successful_status_code
        )

        return response

    def update(
        self,
        path_params: dict,
        payload,
        headers=None,
        expected_successful_status_code=200,
    ):
        endpoint = self.__generate_endpoint(path_params)

        response = self.api_client.patch(
            endpoint, payload, headers, expected_successful_status_code
        )

        return response

    def full_update(
        self,
        path_params: dict,
        payload,
        headers=None,
        expected_successful_status_code=200,
    ):
        endpoint = self.__generate_endpoint(path_params)

        response = self.api_client.put(
            endpoint, payload, headers, expected_successful_status_code
        )

        return response

    def delete(self, path_params: dict, headers=None):

        endpoint = self.__generate_endpoint(path_params)

        self.api_client.delete(endpoint, headers)

    def __generate_endpoint(self, path_params):
        url_parts = []

        parts = self.base_endpoint_template.split("/")

        for part in parts:
            if part.startswith("{") and part.endswith("}"):
                param_name = part[1:-1]

                if param_name in path_params:
                    url_parts.append(str(path_params[param_name]))
            else:
                url_parts.append(part)

        url = "/".join(url_parts)

        return url
