from datetime import date
from unittest import TestCase
from unittest.mock import Mock, patch

from requests.models import Response

from ergani.client import ErganiClient
from ergani.query_models import EssentialTermsAcceptanceStatus


class ExecuteServiceFoundationTests(TestCase):
    def test_execute_service_serializes_parameters(self):
        client = ErganiClient("username", "password", "https://example.test")
        response = Mock(spec=Response)

        with patch.object(client, "_request", return_value=response) as request_mock:
            result = client._execute_service("EX_BASE_06", {"afm": "123456789"})

        self.assertIs(result, response)
        request_mock.assert_called_once_with(
            "POST",
            "/WebServices/ExecuteService",
            {
                "ServiceCode": "EX_BASE_06",
                "Parameters": [
                    {"ParameterName": "afm", "ParameterValue": "123456789"},
                ],
            },
        )


class EssentialTermsAcceptanceTests(TestCase):
    def test_get_essential_terms_acceptance_status_serializes_date_parameter(self):
        client = ErganiClient("username", "password", "https://example.test")
        response = Mock(spec=Response)
        response.json.return_value = {
            "MainStatus": "1",
            "AnswerStatus": "0",
            "AnswerAccept": "2",
        }

        with patch.object(
            client, "_execute_service", return_value=response
        ) as execute_service_mock:
            result = client.get_essential_terms_acceptance_status(
                afm="123456789",
                protocol="1001/12-05-2026",
                effective_date=date(2026, 5, 12),
            )

        self.assertIsInstance(result, EssentialTermsAcceptanceStatus)
        execute_service_mock.assert_called_once_with(
            "EX_BASE_06",
            {
                "afm": "123456789",
                "protocol": "1001/12-05-2026",
                "date": "12/05/2026",
            },
        )

    def test_get_essential_terms_acceptance_status_accepts_dict_payload(self):
        client = ErganiClient("username", "password", "https://example.test")
        response = Mock(spec=Response)
        response.json.return_value = {
            "MainStatus": "1",
            "AnswerStatus": "1",
            "AnswerAccept": "1",
            "AnswerProtocol": "2002/13-05-2026",
            "AnswerDate": "13/05/2026 11:01",
        }

        with patch.object(client, "_execute_service", return_value=response):
            result = client.get_essential_terms_acceptance_status(
                afm="123456789",
                protocol="1001/12-05-2026",
                effective_date=date(2026, 5, 12),
            )

        self.assertEqual(result.main_status_code, "1")
        self.assertEqual(result.answer_status_code, "1")
        self.assertEqual(result.answer_accept_code, "1")
        self.assertEqual(result.answer_protocol, "2002/13-05-2026")
        self.assertEqual(result.answer_date, "13/05/2026 11:01")

    def test_get_essential_terms_acceptance_status_accepts_list_payload(self):
        client = ErganiClient("username", "password", "https://example.test")
        response = Mock(spec=Response)
        response.json.return_value = [
            {
                "MainStatus": "2",
                "AnswerStatus": "0",
                "AnswerAccept": "0",
                "AnswerProtocol": "3003/14-05-2026",
            }
        ]

        with patch.object(client, "_execute_service", return_value=response):
            result = client.get_essential_terms_acceptance_status(
                afm="123456789",
                protocol="1001/12-05-2026",
                effective_date=date(2026, 5, 12),
            )

        self.assertEqual(result.main_status_code, "2")
        self.assertEqual(result.answer_status_code, "0")
        self.assertEqual(result.answer_accept_code, "0")
        self.assertEqual(result.answer_protocol, "3003/14-05-2026")

    def test_get_essential_terms_acceptance_status_keeps_unknown_status_codes(self):
        client = ErganiClient("username", "password", "https://example.test")
        response = Mock(spec=Response)
        response.json.return_value = {
            "MainStatus": "99",
            "AnswerStatus": "7",
            "AnswerAccept": "42",
            "AnswerProtocol": "4004/15-05-2026",
            "AnswerDate": "15/05/2026 10:02",
        }

        with patch.object(client, "_execute_service", return_value=response):
            result = client.get_essential_terms_acceptance_status(
                afm="123456789",
                protocol="1001/12-05-2026",
                effective_date=date(2026, 5, 12),
            )

        self.assertEqual(result.main_status_code, "99")
        self.assertEqual(result.answer_status_code, "7")
        self.assertEqual(result.answer_accept_code, "42")
        self.assertIsNone(result.main_status)
        self.assertIsNone(result.answer_status)
        self.assertIsNone(result.answer_accept)
