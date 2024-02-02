from typing import Optional

import requests
from requests.auth import AuthBase
from requests.models import PreparedRequest

from ergani.exceptions import AuthenticationError
from ergani.utils import extract_error_message


class ErganiAuthentication(AuthBase):
    """
    Authentication handler for the Ergani API
    """

    def __init__(
        self,
        username: str,
        password: str,
        base_url: Optional[str] = "https://trialeservices.yeka.gr/WebServicesAPI/api",
    ) -> None:
        self.username = username
        self.password = password
        self.base_url = base_url
        self.access_token = self._authenticate()

    def __call__(self, request: PreparedRequest) -> PreparedRequest:
        request.headers["Authorization"] = f"Bearer {self.access_token}"
        return request

    def _authenticate(self) -> str:
        endpoint = "/Authentication"
        payload = {
            "Username": self.username,
            "Password": self.password,
            "UserType": "01",
        }

        response = requests.post(f"{self.base_url}{endpoint}", json=payload)

        if response.status_code != 200:
            error_message = extract_error_message(response)
            raise AuthenticationError(message=error_message, response=response)

        token = response.json()["accessToken"]
        return token
