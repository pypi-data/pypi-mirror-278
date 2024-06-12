from requests.exceptions import RequestException, HTTPError


class DixaRequestException(RequestException):
    """Dixa request exception."""

    pass


class DixaHTTPError(HTTPError):
    """Dixa HTTP error."""

    pass


class DixaAPIError(Exception):
    """Dixa API error."""

    pass
