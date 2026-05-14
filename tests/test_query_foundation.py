from datetime import date
from unittest import TestCase
from unittest.mock import Mock, patch

from requests.models import Response

from ergani.client import ErganiClient


class CurrentWorkStatusTests(TestCase):
    def test_get_current_work_status_serializes_parameters(self):
        client = ErganiClient("username", "password", "https://example.test")
        response = Mock(spec=Response)
        response.json.return_value = [
            {
                "WorkSlotStart": "08:00",
                "WorkSlotEnd": "16:00",
                "BreakMinutes": 30,
                "BreakPlacement": "MIDDLE",
                "WorkTypeCode": "REG",
            }
        ]

        with patch.object(
            client, "_execute_service", return_value=response
        ) as execute_service_mock:
            result = client.get_current_work_status(
                branch_number=42,
                target_date=date(2026, 5, 14),
            )

        execute_service_mock.assert_called_once_with(
            "EX_BASE_08",
            {
                "PararthmaAa": 42,
                "Date": "14/05/2026",
            },
        )
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].work_slot_start, "08:00")

    def test_get_current_work_status_raises_on_non_list_response(self):
        client = ErganiClient("username", "password", "https://example.test")
        response = Mock(spec=Response)
        response.json.return_value = {
            "WorkSlotStart": "08:00",
            "WorkSlotEnd": "16:00",
        }

        with patch.object(client, "_execute_service", return_value=response):
            with self.assertRaises(ValueError) as error:
                client.get_current_work_status(
                    branch_number=42,
                    target_date=date(2026, 5, 14),
                )

        self.assertEqual(
            str(error.exception),
            "EX_BASE_08 response payload must be a list",
        )

    def test_get_current_work_status_parses_break_work_type_and_extra_aliases(self):
        client = ErganiClient("username", "password", "https://example.test")
        response = Mock(spec=Response)
        response.json.return_value = [
            {
                "StartTime": "09:00",
                "EndTime": "17:00",
                "breakDurationMinutes": "45",
                "breakPosition": "END",
                "typeCode": "SHIFT_A",
                "extra": {"source": "alias-lower"},
            }
        ]

        with patch.object(client, "_execute_service", return_value=response):
            result = client.get_current_work_status(
                branch_number=42,
                target_date=date(2026, 5, 14),
            )

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].work_slot_start, "09:00")
        self.assertEqual(result[0].work_slot_end, "17:00")
        self.assertEqual(result[0].break_minutes, 45)
        self.assertEqual(result[0].break_placement, "END")
        self.assertEqual(result[0].work_type_code, "SHIFT_A")
        self.assertEqual(result[0].extra, {"source": "alias-lower"})
        self.assertEqual(result[0].raw_payload, response.json.return_value[0])
