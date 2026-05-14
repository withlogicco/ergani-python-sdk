from dataclasses import dataclass
from datetime import date, datetime, timezone
from unittest import TestCase
from unittest.mock import Mock, patch

from requests.models import Response

from ergani.client import ErganiClient
from ergani.query_models import parse_query_list, parse_query_object
from ergani.utils import (
    parse_bool,
    parse_date,
    parse_datetime,
    parse_int,
    parse_list,
    parse_status_code,
)


@dataclass
class DummyQueryRequest:
    value: int

    def serialize(self):
        return {"value": self.value}


class QueryFoundationTests(TestCase):
    def test_query_service_serializes_request_objects_and_parses_payload(self):
        client = ErganiClient("username", "password", "https://example.test")
        response = Mock(spec=Response)
        response.json.return_value = {"value": "7"}

        with patch.object(client, "_request", return_value=response) as request_mock:
            result = client._query_service(
                "EX_BASE_04",
                DummyQueryRequest(value=7),
                parser=lambda payload: parse_int(payload["value"]),
            )

        self.assertEqual(result, 7)
        request_mock.assert_called_once_with(
            "POST", "/WebServices/EX_BASE_04", {"value": 7}
        )

    def test_query_service_can_return_raw_response(self):
        client = ErganiClient("username", "password", "https://example.test")
        response = Mock(spec=Response)

        with patch.object(client, "_request", return_value=response) as request_mock:
            result = client._query_service("EX_BASE_01", method="GET", raw_response=True)

        self.assertIs(result, response)
        request_mock.assert_called_once_with("GET", "/WebServices/EX_BASE_01", None)

    def test_get_services_list_uses_get_request(self):
        client = ErganiClient("username", "password", "https://example.test")
        response = Mock(spec=Response)

        with patch.object(client, "_request", return_value=response) as request_mock:
            result = client.get_services_list()

        self.assertIs(result, response)
        request_mock.assert_called_once_with("GET", "/WebServices/ServicesList", None)

    def test_parse_helpers_cover_common_query_scalars(self):
        parsed_datetime = parse_datetime("2026-05-14T08:30:00Z")

        self.assertEqual(parse_date("14/05/2026"), date(2026, 5, 14))
        self.assertEqual(
            parsed_datetime, datetime(2026, 5, 14, 8, 30, tzinfo=timezone.utc)
        )
        self.assertEqual(parse_int("42"), 42)
        self.assertEqual(parse_bool("1"), True)
        self.assertEqual(parse_status_code(True), "1")
        self.assertEqual(parse_list(None), [])

    def test_query_model_helpers_validate_payload_shape(self):
        payload = [{"code": "01"}, {"code": 2}]
        result = parse_query_list(
            payload,
            lambda item: parse_status_code(item["code"]),
        )

        self.assertEqual(result, ["01", "2"])
        self.assertEqual(
            parse_query_object({"status": 1}, lambda item: parse_status_code(item["status"])),
            "1",
        )

        with self.assertRaises(ValueError):
            parse_query_object([], lambda item: item)