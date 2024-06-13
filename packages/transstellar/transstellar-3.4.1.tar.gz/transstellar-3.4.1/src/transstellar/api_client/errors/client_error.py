from requests.exceptions import RequestException

class ClientError(RequestException):
    pass
