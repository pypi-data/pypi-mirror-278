from requests.exceptions import RequestException

class ServerError(RequestException):
    pass
