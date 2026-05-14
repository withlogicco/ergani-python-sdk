from unittest import TestCase
from unittest.mock import Mock, patch

from requests.models import Response

from ergani.client import ErganiClient
from ergani.query_models import ParameterOption, parse_parameter_options


class ExecuteServiceFoundationTests(TestCase):
    def test_execute_service_serializes_parameters(self):
        client = ErganiClient("username", "password", "https://example.test")
        response = Mock(spec=Response)

        with patch.object(client, "_request", return_value=response) as request_mock:
            result = client._execute_service("EX_BASE_03", {"Parameter": "Sepe"})

        self.assertIs(result, response)
        request_mock.assert_called_once_with(
            "POST",
            "/WebServices/ExecuteService",
            {
                "ServiceCode": "EX_BASE_03",
                "Parameters": [
                    {"ParameterName": "Parameter", "ParameterValue": "Sepe"},
                ],
            },
        )


class ParameterCatalogTests(TestCase):
    def test_get_parameters_serializes_allowed_catalog_values(self):
        client = ErganiClient("username", "password", "https://example.test")

        for catalog in ["Sepe", "KallikratisDhmos", "WorkCardDelayReason"]:
            response = Mock(spec=Response)
            response.json.return_value = []

            with self.subTest(catalog=catalog):
                with patch.object(
                    client, "_request", return_value=response
                ) as request_mock:
                    result = client.get_parameters(catalog)

                self.assertEqual(result, [])
                request_mock.assert_called_once_with(
                    "POST",
                    "/WebServices/ExecuteService",
                    {
                        "ServiceCode": "EX_BASE_03",
                        "Parameters": [
                            {
                                "ParameterName": "Parameter",
                                "ParameterValue": catalog,
                            },
                        ],
                    },
                )

    def test_get_parameters_rejects_non_list_response(self):
        client = ErganiClient("username", "password", "https://example.test")
        response = Mock(spec=Response)
        response.json.return_value = {"unexpected": {"Code": "A"}}

        with patch.object(client, "_execute_service", return_value=response):
            with self.assertRaisesRegex(
                ValueError, "parameter options response to be a list"
            ):
                client.get_parameters("Sepe")

    def test_get_parameters_parses_wrapped_concrete_payload(self):
        client = ErganiClient("username", "password", "https://example.test")
        response = Mock(spec=Response)
        response.json.return_value = {
            "EX_BASE_03": {
                "Param": [
                    {
                        "Code": "001",
                        "Description": "ΠΡΟΒΛΗΜΑ ΣΤΗΝ ΗΛΕΚΤΡΟΔΟΤΗΣΗ/ΤΗΛΕΠΙΚΟΙΝΩΝΙΕΣ",
                        "Extra": None,
                    }
                ]
            }
        }

        with patch.object(client, "_execute_service", return_value=response):
            result = client.get_parameters("WorkCardDelayReason")

        self.assertEqual(
            result,
            [
                ParameterOption(
                    code="001",
                    value="ΠΡΟΒΛΗΜΑ ΣΤΗΝ ΗΛΕΚΤΡΟΔΟΤΗΣΗ/ΤΗΛΕΠΙΚΟΙΝΩΝΙΕΣ",
                    description="ΠΡΟΒΛΗΜΑ ΣΤΗΝ ΗΛΕΚΤΡΟΔΟΤΗΣΗ/ΤΗΛΕΠΙΚΟΙΝΩΝΙΕΣ",
                    extra=None,
                )
            ],
        )

    def test_parse_parameter_options_supports_field_aliases(self):
        result = parse_parameter_options(
            [
                {
                    "Code": "01",
                    "Value": "SEPE",
                    "Description": "Inspectorate",
                },
                {
                    "Id": 7,
                    "Name": "Athens",
                    "Label": "Municipality of Athens",
                },
                {
                    "key": "LATE",
                    "title": "Delay",
                    "text": "Work card delayed submission",
                },
            ]
        )

        self.assertEqual(
            result,
            [
                ParameterOption(code="01", value="SEPE", description="Inspectorate"),
                ParameterOption(
                    code="7",
                    value="Athens",
                    description="Municipality of Athens",
                ),
                ParameterOption(
                    code="LATE",
                    value="Delay",
                    description="Work card delayed submission",
                ),
            ],
        )
