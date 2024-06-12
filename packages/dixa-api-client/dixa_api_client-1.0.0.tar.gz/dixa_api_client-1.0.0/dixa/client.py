import logging
import time
from enum import Enum

from requests import Request, Response
from requests.exceptions import HTTPError, JSONDecodeError, RequestException
from requests.models import PreparedRequest
from requests.sessions import Session

from .exceptions import DixaAPIError, DixaHTTPError, DixaRequestException
from .model import DixaAPIResponse


class RequestMethod(Enum):
    """HTTP request methods."""

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


class DixaClient:
    """Dixa API client."""

    def __init__(
        self,
        api_key: str,
        api_secret: str | None = None,
        max_retries: int = 3,
        retry_delay: int = 10,
        logger: logging.Logger | None = None,
    ):
        """Initializes the Dixa API client."""

        self._api_secret = api_secret
        self._max_retries = max_retries
        self._retry_delay = retry_delay
        self._retries = 0
        self._logger = logger or logging.getLogger(__name__)

        self._session = Session()
        self._session.headers.update(
            {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": api_key,
            }
        )

    def _redact_auth(self, request: PreparedRequest) -> PreparedRequest:
        """Redacts the Authorization header from a request."""

        temp_request = request.copy()
        temp_request.headers["Authorization"] = "REDACTED"
        return temp_request

    def _retry(self, request: PreparedRequest) -> DixaAPIResponse:
        """Retries a request."""

        if self._retries >= self._max_retries:
            self._logger.error(
                "Max retries reached", extra={"request": self._redact_auth(request)}
            )
            raise DixaAPIError("Max retries reached")

        self._retries += 1
        self._logger.info(
            "Retrying",
            extra={
                "retries": self._retries,
                "max_retries": self._max_retries,
                "delay": self._retry_delay,
                "request": self._redact_auth(request),
            },
        )
        time.sleep(self._retry_delay)
        return self._send(request)

    def _extract_error_message(self, response: Response) -> str:
        """Extracts an error message from a response."""

        try:
            error_response = response.json()
            return error_response.get("message")
        except JSONDecodeError:
            self._logger.error(
                "Failed to decode JSON response", extra={"response": response.text}
            )
            return response.text

    def _extract_data(self, response: Response) -> DixaAPIResponse:
        """Extracts data from a response."""

        try:
            data = response.json()
            return data
        except JSONDecodeError:
            self._logger.error(
                "Failed to decode JSON response", extra={"response": response.text}
            )
            return {"data": {}}

    def _send(self, request: PreparedRequest) -> DixaAPIResponse:
        """Sends a request and handles retries and errors."""

        self._logger.debug(
            "Sending request", extra={"request": self._redact_auth(request)}
        )
        try:
            response = self._session.send(request)

            if response.status_code == 429:
                self._logger.warning(
                    "Rate limited, retrying...", extra={"response": response}
                )
                return self._retry(request)

            if response.status_code >= 500:
                self._logger.error(
                    "Server error, retrying...", extra={"response": response}
                )
                return self._retry(request)

            self._retries = 0
            response.raise_for_status()

            data = self._extract_data(response)
            self._logger.debug("Request successful", extra={"response": data})
            return data

        except HTTPError as http_error:
            self._logger.error("HTTP error", extra={"error": http_error})
            raise DixaHTTPError(
                self._extract_error_message(http_error.response)
            ) from http_error
        except RequestException as request_error:
            self._logger.error("Request failed", extra={"error": request_error})
            raise DixaRequestException("Request failed") from request_error

    def _request(
        self,
        method: RequestMethod,
        url: str,
        query: dict | None = None,
        json: dict | None = None,
    ) -> DixaAPIResponse:
        """Creates and sends a request."""

        request = Request(method.value, url, params=query, json=json)
        prepared_request = self._session.prepare_request(request)

        return self._send(prepared_request)

    def get(self, url: str, query: dict | None = None) -> DixaAPIResponse:
        """Sends a GET request."""

        return self._request(RequestMethod.GET, url, query=query)

    def post(self, url: str, json: dict | None = None) -> DixaAPIResponse:
        """Sends a POST request."""

        return self._request(RequestMethod.POST, url, json=json)

    def put(self, url: str, json: dict | None = None) -> DixaAPIResponse:
        """Sends a PUT request."""

        return self._request(RequestMethod.PUT, url, json=json)

    def delete(self, url: str, json: dict | None = None) -> DixaAPIResponse:
        """Sends a DELETE request."""

        return self._request(RequestMethod.DELETE, url, json=json)

    def patch(self, url: str, json: dict | None = None) -> DixaAPIResponse:
        """Sends a PATCH request."""

        return self._request(RequestMethod.PATCH, url, json=json)
