from unittest import TestCase
from unittest.mock import Mock, patch

from requests.models import Response

from ergani.client import ErganiClient
from ergani.query_models import (
    MonthlyStatusRecord,
    MonthlyStatusRequest,
    parse_monthly_status_list,
)
from ergani.utils import normalize_base_url


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

    def test_normalize_base_url_keeps_v2_host_root_url(self):
        self.assertEqual(
            normalize_base_url("https://trialv2eservices.yeka.gr/"),
            "https://trialv2eservices.yeka.gr",
        )

    def test_normalize_base_url_keeps_existing_api_path(self):
        self.assertEqual(
            normalize_base_url("https://example.test/WebServicesAPI/api"),
            "https://example.test/WebServicesAPI/api",
        )


class MonthlyStatusTests(TestCase):
    def test_monthly_status_request_serializes_expected_payload(self):
        request = MonthlyStatusRequest(report_year=2026, report_month=4)

        self.assertEqual(
            request.serialize(),
            {"ReportYear": 2026, "ReportMonth": 4},
        )

    def test_monthly_status_request_validates_month_range_and_year_bounds(self):
        with self.assertRaisesRegex(
            ValueError, "report_month must be between 1 and 12"
        ):
            MonthlyStatusRequest(report_year=2026, report_month=0)

        with self.assertRaisesRegex(
            ValueError, "report_month must be between 1 and 12"
        ):
            MonthlyStatusRequest(report_year=2026, report_month=13)

        with self.assertRaisesRegex(
            ValueError, "report_year must be between 2000 and 2100"
        ):
            MonthlyStatusRequest(report_year=1999, report_month=4)

        with self.assertRaisesRegex(
            ValueError, "report_year must be between 2000 and 2100"
        ):
            MonthlyStatusRequest(report_year=2101, report_month=4)

    def test_parse_monthly_status_list_wraps_raw_records(self):
        result = parse_monthly_status_list(
            [
                {"EmployeeAfm": "123456789", "Status": "1"},
                {"EmployeeAfm": "987654321", "Status": "2"},
            ]
        )

        self.assertEqual(
            result,
            [
                MonthlyStatusRecord(
                    raw_payload={"EmployeeAfm": "123456789", "Status": "1"}
                ),
                MonthlyStatusRecord(
                    raw_payload={"EmployeeAfm": "987654321", "Status": "2"}
                ),
            ],
        )

        with self.assertRaisesRegex(
            ValueError, "Expected monthly status record to be an object"
        ):
            parse_monthly_status_list(["unexpected"])

    def test_get_monthly_status_executes_service_and_parses_json(self):
        client = ErganiClient("username", "password", "https://example.test")
        response = Mock(spec=Response)
        response.json.return_value = [
            {"EmployeeAfm": "123456789", "Status": "1"},
        ]

        with patch.object(client, "_request", return_value=response) as request_mock:
            result = client.get_monthly_status(report_year=2026, report_month=4)

        self.assertEqual(
            result,
            [
                MonthlyStatusRecord(
                    raw_payload={"EmployeeAfm": "123456789", "Status": "1"}
                )
            ],
        )
        request_mock.assert_called_once_with(
            "POST",
            "/WebServices/ExecuteService",
            {
                "ServiceCode": "EX_BASE_04",
                "Parameters": [
                    {"ParameterName": "ReportYear", "ParameterValue": 2026},
                    {"ParameterName": "ReportMonth", "ParameterValue": 4},
                ],
            },
        )

    def test_get_monthly_status_returns_empty_list_for_no_content(self):
        client = ErganiClient("username", "password", "https://example.test")

        with patch.object(client, "_execute_service", return_value=None):
            result = client.get_monthly_status(report_year=2026, report_month=4)

        self.assertEqual(result, [])

    def test_get_monthly_status_rejects_non_json_response(self):
        client = ErganiClient("username", "password", "https://example.test")
        response = Mock(spec=Response)
        response.json.side_effect = ValueError("invalid json")

        with patch.object(client, "_execute_service", return_value=response):
            with self.assertRaisesRegex(
                ValueError, "EX_BASE_04 returned a non-JSON response"
            ):
                client.get_monthly_status(report_year=2026, report_month=4)
