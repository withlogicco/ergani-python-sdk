from unittest import TestCase
from unittest.mock import Mock, patch

from requests.models import Response

from ergani.client import ErganiClient


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

    @patch("ergani.client.ErganiAuthentication")
    @patch("ergani.client.requests.request")
    def test_request_passes_payload_to_response_handler(
        self,
        request_mock: Mock,
        auth_mock: Mock,
    ) -> None:
        raw_response = Mock(spec=Response)
        handled_response = Mock(spec=Response)
        request_mock.return_value = raw_response
        auth_mock.return_value = Mock()
        client = ErganiClient("user", "pass", "https://example.com/WebServicesAPI/api")
        payload = {"ServiceCode": "EX_BASE_01", "Parameters": []}

        with patch.object(
            client,
            "_handle_response",
            return_value=handled_response,
        ) as handle_response_mock:
            result = client._request("POST", "WebServices/ExecuteService", payload)

        self.assertIs(result, handled_response)
        request_mock.assert_called_once_with(
            "POST",
            "https://example.com/WebServicesAPI/api/WebServices/ExecuteService",
            json=payload,
            auth=auth_mock.return_value,
        )
        handle_response_mock.assert_called_once_with(raw_response, payload)
