from unittest import TestCase
from unittest.mock import Mock

from requests.models import Response

from ergani.utils import extract_error_message, normalize_base_url


class NormalizeBaseUrlTests(TestCase):
    def test_rejects_empty_base_url(self) -> None:
        with self.assertRaises(ValueError):
            normalize_base_url("")

    def test_rejects_none_base_url(self) -> None:
        with self.assertRaises(ValueError):
            normalize_base_url(None)

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


class ExtractErrorMessageTests(TestCase):
    def test_returns_message_from_json_payload(self) -> None:
        response = Mock(spec=Response)
        response.headers = {"Content-Type": "application/json"}
        response.json.return_value = {"message": "invalid credentials"}

        self.assertEqual(extract_error_message(response), "invalid credentials")

    def test_returns_plain_text_body(self) -> None:
        response = Mock(spec=Response)
        response.headers = {"Content-Type": "text/plain"}
        response.text = "service unavailable\n"

        self.assertEqual(extract_error_message(response), "service unavailable")
