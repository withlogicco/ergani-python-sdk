from unittest import TestCase
from unittest.mock import Mock, patch

from requests.models import Response

from ergani.client import ErganiClient
from ergani.models import EmployerDetails, parse_employer_details


class EmployerDetailsTests(TestCase):
    def test_get_employer_details_uses_execute_service_and_parses_verified_fields(self):
        client = ErganiClient("username", "password", "https://example.test")
        response = Mock(spec=Response)
        response.json.return_value = {
            "EX_BASE_01": {
                "Ergodotis": {
                    "Id": "33263",
                    "Afm": "801405734",
                    "Eponimia": "LOGIC ΜΟΝΟΠΡΟΣΩΠΗ ΙΚΕ",
                    "DiakritikosTitlos": "LOGIC",
                    "Ame": "9316208810",
                    "IsInCardSector": "1",
                }
            }
        }

        with patch.object(
            client, "_execute_service", return_value=response
        ) as execute_service_mock:
            result = client.get_employer_details()

        self.assertEqual(
            result,
            EmployerDetails(
                employer_id=33263,
                employer_tax_identification_number="801405734",
                name="LOGIC ΜΟΝΟΠΡΟΣΩΠΗ ΙΚΕ",
                distinctive_title="LOGIC",
                employer_registry_number="9316208810",
                is_in_card_sector=True,
                raw_payload={
                    "Id": "33263",
                    "Afm": "801405734",
                    "Eponimia": "LOGIC ΜΟΝΟΠΡΟΣΩΠΗ ΙΚΕ",
                    "DiakritikosTitlos": "LOGIC",
                    "Ame": "9316208810",
                    "IsInCardSector": "1",
                },
            ),
        )
        execute_service_mock.assert_called_once_with("EX_BASE_01")

    def test_employer_details_parse_reads_verified_fields(self):
        self.assertEqual(
            EmployerDetails.parse(
                {
                    "EX_BASE_01": {
                        "Ergodotis": {
                            "Id": "33263",
                            "Afm": "801405734",
                            "Eponimia": "LOGIC ΜΟΝΟΠΡΟΣΩΠΗ ΙΚΕ",
                            "DiakritikosTitlos": "LOGIC",
                            "Ame": "9316208810",
                            "IsInCardSector": "1",
                        }
                    }
                }
            ),
            EmployerDetails(
                employer_id=33263,
                employer_tax_identification_number="801405734",
                name="LOGIC ΜΟΝΟΠΡΟΣΩΠΗ ΙΚΕ",
                distinctive_title="LOGIC",
                employer_registry_number="9316208810",
                is_in_card_sector=True,
                raw_payload={
                    "Id": "33263",
                    "Afm": "801405734",
                    "Eponimia": "LOGIC ΜΟΝΟΠΡΟΣΩΠΗ ΙΚΕ",
                    "DiakritikosTitlos": "LOGIC",
                    "Ame": "9316208810",
                    "IsInCardSector": "1",
                },
            ),
        )

    def test_parse_employer_details_keeps_verified_fields_optional(self):
        self.assertEqual(
            parse_employer_details({}),
            EmployerDetails(raw_payload={}),
        )

    def test_parse_employer_details_handles_false_card_sector_values(self):
        self.assertEqual(
            parse_employer_details(
                {"EX_BASE_01": {"Ergodotis": {"IsInCardSector": "0"}}}
            ),
            EmployerDetails(
                is_in_card_sector=False,
                raw_payload={"IsInCardSector": "0"},
            ),
        )

    def test_parse_employer_details_keeps_unknown_card_sector_values_optional(self):
        self.assertEqual(
            parse_employer_details(
                {"EX_BASE_01": {"Ergodotis": {"IsInCardSector": "yes"}}}
            ),
            EmployerDetails(
                raw_payload={"IsInCardSector": "yes"},
            ),
        )

    def test_parse_employer_details_requires_object_payload(self):
        with self.assertRaises(ValueError):
            parse_employer_details([])
