from typing import Optional

import requests
from requests.auth import AuthBase
from requests.exceptions import RequestException
from requests.models import PreparedRequest

from ergani.exceptions import AuthenticationError
from ergani.utils import extract_error_message


class ErganiAuthentication(AuthBase):
    """
    Authentication handler for the Ergani API.
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

    def _authenticate(self) -> Optional[str]:
        endpoint = "/Authentication"
        payload = {
            "Username": self.username,
            "Password": self.password,
            "UserType": "01",
        }

        auth_headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(
                f"{self.base_url}{endpoint}", json=payload, headers=auth_headers
            )
            print(response.json())
            if response.status_code != 200:
                error_message = extract_error_message(response)
                raise AuthenticationError(message=error_message, response=response)

            token = response.json().get("accessToken")
            return token
        except RequestException:
            raise AuthenticationError()
