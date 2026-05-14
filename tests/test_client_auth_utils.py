from unittest import TestCase
from unittest.mock import Mock, patch

from requests.models import Response

from ergani.auth import ErganiAuthentication
from ergani.client import ErganiClient
from ergani.exceptions import AuthenticationError
from ergani.utils import normalize_base_url


class NormalizeBaseUrlTests(TestCase):
    def test_rejects_empty_base_url(self) -> None:
        with self.assertRaises(ValueError):
            normalize_base_url("")

    def test_trims_trailing_slash(self) -> None:
        normalized = normalize_base_url("https://example.com/WebServicesAPI/api/")

        self.assertEqual(normalized, "https://example.com/WebServicesAPI/api")

    def test_preserves_non_api_paths(self) -> None:
        normalized = normalize_base_url("https://example.com/custom/path/")

        self.assertEqual(
            normalized,
            "https://example.com/custom/path",
        )

    def test_preserves_existing_api_path(self) -> None:
        normalized = normalize_base_url("https://example.com/WebServicesAPI/api")

        self.assertEqual(
            normalized,
            "https://example.com/WebServicesAPI/api",
        )

    def test_trims_surrounding_whitespace(self) -> None:
        normalized = normalize_base_url("  https://example.com/custom/path/  ")

        self.assertEqual(
            normalized,
            "https://example.com/custom/path",
        )


class ErganiClientRequestTests(TestCase):
    @patch("ergani.client.ErganiAuthentication")
    @patch("ergani.client.requests.request")
    def test_request_strips_leading_slash_from_endpoint(
        self,
        request_mock: Mock,
        auth_mock: Mock,
    ) -> None:
        response = Mock(spec=Response)
        response.status_code = 200
        response.raise_for_status.return_value = None
        request_mock.return_value = response
        auth_mock.return_value = Mock()

        client = ErganiClient("user", "pass", "https://example.com/WebServicesAPI/api")

        client._request("GET", "/WebServices/ServicesList")

        request_mock.assert_called_once_with(
            "GET",
            "https://example.com/WebServicesAPI/api/WebServices/ServicesList",
            json=None,
            auth=auth_mock.return_value,
        )


class ErganiAuthenticationTests(TestCase):
    @patch("ergani.auth.requests.post")
    def test_authenticate_raises_authentication_error_when_access_token_missing(
        self,
        post_mock: Mock,
    ) -> None:
        response = Mock(spec=Response)
        response.status_code = 200
        response.text = '{"message":"missing token"}'
        response.headers = {"Content-Type": "application/json"}
        response.json.return_value = {"message": "missing token"}
        post_mock.return_value = response

        with self.assertRaises(AuthenticationError) as context:
            ErganiAuthentication(
                "user", "pass", "https://example.com/WebServicesAPI/api"
            )

        self.assertEqual(context.exception.message, "missing token")
