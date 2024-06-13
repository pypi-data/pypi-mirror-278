from requests.exceptions import RequestException

class UnauthorizedError(RequestException):
    pass
