from typing import Any, Dict, Optional

from requests.models import Response


class Error(Exception):
    """
    Base class for all API errors
    """

    def __init__(
        self,
        message: Optional[str] = None,
        response: Optional[Response] = None,
        payload: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.message = message
        self.response = response
        self.payload = payload

    def __str__(self) -> str:
        if self.response:
            if not self.message:
                if self.response.status_code >= 500:
                    self.message = "Service unavailable, please try again later"
                if self.response.status_code == 400:
                    self.message = "Please check your inputs and try again"

            return f"Status code {self.response.status_code}. Error message: {self.message}"

        return f"Error message: {self.message}"


class AuthenticationError(Error):
    """
    Raised when an API request fails due to an authentication error
    """

    pass


class APIError(Error):
    """
    Raised when an API request fails due to an unknown error
    """

    pass
