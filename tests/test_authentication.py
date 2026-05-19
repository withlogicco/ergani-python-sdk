from unittest import TestCase
from unittest.mock import Mock, patch

from requests.models import PreparedRequest, Response

from ergani.auth import ErganiAuthentication
from ergani.exceptions import AuthenticationError


class ErganiAuthenticationTests(TestCase):
    @patch("ergani.auth.requests.post")
    def test_authenticate_raises_authentication_error_when_access_token_missing(
        self,
        post_mock: Mock,
    ) -> None:
        response = Mock(spec=Response)
        response.status_code = 200
        response.text = '{"message":"missing token"}'
        response.headers = {"Content-Type": "application/json"}
        response.json.return_value = {"message": "missing token"}
        post_mock.return_value = response

        with self.assertRaises(AuthenticationError) as context:
            ErganiAuthentication(
                "user", "pass", "https://example.com/WebServicesAPI/api"
            )

        self.assertEqual(context.exception.message, "missing token")

    @patch("ergani.auth.requests.post")
    def test_authenticate_raises_authentication_error_for_non_200_response(
        self,
        post_mock: Mock,
    ) -> None:
        response = Mock(spec=Response)
        response.status_code = 401
        response.text = "unauthorized"
        response.headers = {"Content-Type": "text/plain"}
        post_mock.return_value = response

        with self.assertRaises(AuthenticationError) as context:
            ErganiAuthentication(
                "user", "pass", "https://example.com/WebServicesAPI/api"
            )

        self.assertEqual(context.exception.message, "unauthorized")

    @patch.object(ErganiAuthentication, "_authenticate", return_value="token-123")
    def test_call_adds_bearer_token_header(self, authenticate_mock: Mock) -> None:
        auth = ErganiAuthentication(
            "user", "pass", "https://example.com/WebServicesAPI/api"
        )
        request = PreparedRequest()
        request.prepare(method="GET", url="https://example.com/resource")

        authenticated_request = auth(request)

        self.assertIs(authenticated_request, request)
        self.assertEqual(request.headers["Authorization"], "Bearer token-123")
        authenticate_mock.assert_called_once_with()
