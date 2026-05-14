from datetime import date
from unittest import TestCase
from unittest.mock import Mock, patch

from requests.models import Response

from ergani.client import ErganiClient


class ActualWorkLogTests(TestCase):
    def test_get_actual_work_log_serializes_parameters(self):
        client = ErganiClient("username", "password", "https://example.test")
        response = Mock(spec=Response)
        response.json.return_value = [
            {
                "Afm": "123456789",
                "EmployeeName": "Jane Doe",
                "StartTime": "08:00",
                "EndTime": "16:00",
                "Overnight": "0",
            }
        ]

        with patch.object(
            client, "_execute_service", return_value=response
        ) as execute_service_mock:
            result = client.get_actual_work_log(
                branch_number=7,
                target_date=date(2026, 5, 14),
            )

        execute_service_mock.assert_called_once_with(
            "EX_BASE_07",
            {
                "PararthmaAa": 7,
                "Date": "14/05/2026",
            },
        )
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].employee_afm, "123456789")

    def test_get_actual_work_log_raises_on_non_list_response(self):
        client = ErganiClient("username", "password", "https://example.test")
        response = Mock(spec=Response)
        response.json.return_value = {
            "Afm": "123456789",
            "EmployeeName": "Jane Doe",
        }

        with patch.object(client, "_execute_service", return_value=response):
            with self.assertRaises(ValueError) as error:
                client.get_actual_work_log(
                    branch_number=7,
                    target_date=date(2026, 5, 14),
                )

        self.assertEqual(
            str(error.exception),
            "EX_BASE_07 response payload must be a list",
        )

    def test_get_actual_work_log_normalizes_overnight_aliases(self):
        client = ErganiClient("username", "password", "https://example.test")
        response = Mock(spec=Response)
        response.json.return_value = [
            {
                "Afm": "123456789",
                "EmployeeName": "John Doe",
                "StartTime": "22:00",
                "EndTime": "06:00",
                "Overnight": "YES",
            },
            {
                "Afm": "987654321",
                "EmployeeName": "Jane Doe",
                "StartTime": "09:00",
                "EndTime": "17:00",
                "Overnight": "false",
            },
        ]

        with patch.object(client, "_execute_service", return_value=response):
            result = client.get_actual_work_log(
                branch_number=7,
                target_date=date(2026, 5, 14),
            )

        self.assertEqual(result[0].overnight, True)
        self.assertEqual(result[1].overnight, False)
