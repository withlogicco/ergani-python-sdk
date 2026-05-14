from unittest import TestCase
from unittest.mock import Mock, patch

from requests.models import Response

from ergani.client import ErganiClient


class ExecuteServiceFoundationTests(TestCase):
    def test_execute_service_serializes_parameters(self):
        client = ErganiClient("username", "password", "https://example.test")
        response = Mock(spec=Response)

        with patch.object(client, "_request", return_value=response) as request_mock:
            result = client._execute_service("EX_BASE_04", {"ReportYear": 2026})

        self.assertIs(result, response)
        request_mock.assert_called_once_with(
            "POST",
            "/WebServices/ExecuteService",
            {
                "ServiceCode": "EX_BASE_04",
                "Parameters": [
                    {"ParameterName": "ReportYear", "ParameterValue": 2026},
                ],
            },
        )

    def test_execute_service_uses_empty_parameter_array_by_default(self):
        client = ErganiClient("username", "password", "https://example.test")
        response = Mock(spec=Response)

        with patch.object(client, "_request", return_value=response) as request_mock:
            result = client._execute_service("EX_BASE_01")

        self.assertIs(result, response)
        request_mock.assert_called_once_with(
            "POST",
            "/WebServices/ExecuteService",
            {"ServiceCode": "EX_BASE_01", "Parameters": []},
        )

    def test_get_services_list_uses_get_request(self):
        client = ErganiClient("username", "password", "https://example.test")
        response = Mock(spec=Response)

        with patch.object(client, "_request", return_value=response) as request_mock:
            result = client.get_services_list()

        self.assertIs(result, response)
        request_mock.assert_called_once_with("GET", "/WebServices/ServicesList", None)
