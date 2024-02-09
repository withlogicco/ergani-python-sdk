from datetime import datetime
from typing import Any, Dict, List, Optional

import requests
from requests.models import Response

from ergani.auth import ErganiAuthentication
from ergani.exceptions import APIError, AuthenticationError
from ergani.models import (
    CompanyDailySchedule,
    CompanyOvertime,
    CompanyWeeklySchedule,
    CompanyWorkCard,
    SubmissionResponse,
)
from ergani.utils import extract_error_message


class ErganiClient:
    """
    A client for interacting with the Ergani API

    Args:
        username str: The username for authentication with Ergani
        password str: The password for authentication with Ergani
        base_url str: The base URL of the Ergani API. Defaults to "https://trialeservices.yeka.gr/WebServicesAPI/api".
    """

    def __init__(
        self,
        username: str,
        password: str,
        base_url: Optional[str] = "https://trialeservices.yeka.gr/WebServicesAPI/api",
    ) -> None:
        self.username = username
        self.password = password
        self.base_url = base_url

    def _request(
        self, method: str, endpoint: str, payload: Optional[Dict[str, Any]] = None
    ) -> Optional[Response]:
        """
        Sends a request to the specified endpoint using the given HTTP method and payload

        Args:
            method (str): The HTTP method to use for the request (e.g., 'GET', 'POST')
            endpoint (str): The API endpoint to which the request should be sent to
            payload (Optional[Dict[str, Any]]): The JSON-serializable dictionary to be sent as the request payload

        Returns:
            Optional[Response]: The response object from the requests library. Returns None for 204 No Content responses.

        Raises:
            Requests exceptions may be raised for network-related errors
        """

        url = f"{self.base_url}/{endpoint}"
        auth = ErganiAuthentication(self.username, self.password, self.base_url)

        response = requests.request(
            method,
            url,
            json=payload,
            auth=auth,
        )

        return self._handle_response(response, payload)

    def _handle_response(
        self, response: Response, payload: Optional[Dict[str, Any]] = None
    ) -> Optional[Response]:
        """
        Handles the HTTP response, raising exceptions for error status codes and returning the response for successful ones

        Args:
            response (Response): The response object to handle
            payload (Optional[Dict[str, Any]]): The original request payload for inclusion in exceptions if needed

        Returns:
            Optional[Response]: The original response object for successful requests or None for 204 No Content responses

        Raises:
            APIError: An error occurred while communicating with the Ergani API
            AuthenticationError: Raised if there is an authentication error with the Ergani API
        """

        if response.status_code == 401:
            error_message = extract_error_message(response)
            raise AuthenticationError(message=error_message, response=response)

        if response.status_code == 204:
            return None

        try:
            response.raise_for_status()
            return response
        except:
            error_message = extract_error_message(response)
            raise APIError(message=error_message, response=response, payload=payload)

    def _extract_submission_result(
        self, response: Optional[Response]
    ) -> List[SubmissionResponse]:
        """
        Extracts the submission result from the Ergani API response

        Args:
            response (Response): The response object from the Ergani API

        Returns:
            List[SubmissionResponse]: A list of submission responses parsed from the API response

        Raises:
            ValueError: If the response cannot be parsed into submission responses, indicating an unexpected format
        """

        if not response:
            return []

        data = response.json()
        submissions = []

        for submission in data:
            submission_date_str = submission["submitDate"]
            submission_date = datetime.strptime(submission_date_str, "%d/%m/%Y %H:%M")

            submission_response = SubmissionResponse(
                submission_id=submission["id"],
                protocol=submission["protocol"],
                sumbmission_date=submission_date,
            )
            submissions.append(submission_response)

        return submissions

    def submit_work_card(
        self, company_work_cards: List[CompanyWorkCard]
    ) -> List[SubmissionResponse]:
        """
        Submits work card records (check-in, check-out) for employees to the Ergani API

        Args:
            company_work_cards List[CompanyWorkCard]: A list of CompanyWorkCard instances to be submitted

        Returns:
            List[SubmissionResponse]: A list of SumbmissionResponse that were parsed from the API response

        Raises:
            APIError: An error occurred while communicating with the Ergani API
            AuthenticationError: Raised if there is an authentication error with the Ergani API
        """

        endpoint = "/Documents/WRKCardSE"

        request_payload = {
            "Cards": {
                "Card": [
                    company_card.serialize() for company_card in company_work_cards
                ]
            }
        }

        response = self._request("POST", endpoint, request_payload)

        return self._extract_submission_result(response)

    def submit_overtime(
        self, company_overtimes: List[CompanyOvertime]
    ) -> List[SubmissionResponse]:
        """
        Submits overtime records for employees to the Ergani API

        Args:
            company_overtimes List[CompanyOvertime]: A list of CompanyOvertime instances to be submitted

        Returns:
            List[SubmissionResponse]: A list of SumbmissionResponse that were parsed from the API response

        Raises:
            APIError: An error occurred while communicating with the Ergani API
            AuthenticationError: Raised if there is an authentication error with the Ergani API
        """

        endpoint = "/Documents/OvTime"

        request_payload = {
            "Overtimes": {
                "Overtime": [
                    company_overtime.serialize()
                    for company_overtime in company_overtimes
                ]
            }
        }

        response = self._request("POST", endpoint, request_payload)

        return self._extract_submission_result(response)

    def submit_daily_schedule(
        self, company_daily_schedules: List[CompanyDailySchedule]
    ) -> List[SubmissionResponse]:
        """
        Submits schedule records that are updated on a daily basis for employees to the Ergani API

        Args:
            company_daily_schedules List[CompanyDailySchedule]: A list of CompanyDailySchedule instances to be submitted

        Returns:
            List[SubmissionResponse]: A list of SumbmissionResponse that were parsed from the API response

        Raises:
            APIError: An error occurred while communicating with the Ergani API
            AuthenticationError: Raised if there is an authentication error with the Ergani API
        """

        endpoint = "/Documents/WTODaily"

        request_payload = {
            "WTOS": {
                "WTO": [schedule.serialize() for schedule in company_daily_schedules]
            }
        }

        response = self._request("POST", endpoint, request_payload)

        return self._extract_submission_result(response)

    def submit_weekly_schedule(
        self, company_weekly_schedules: List[CompanyWeeklySchedule]
    ) -> List[SubmissionResponse]:
        """
        Submits weekly schedule records for employees to the Ergani API

        Args:
            company_weekly_schedules List[CompanyWeeklySchedule]: A list of CompanyWeeklySchedule instances to be submitted

        Returns:
            List[SubmissionResponse]: A list of SumbmissionResponse that were parsed from the API response

        Raises:
            APIError: An error occurred while communicating with the Ergani API
            AuthenticationError: Raised if there is an authentication error with the Ergani API
        """

        endpoint = "/Documents/WTOWeek"

        request_payload = {
            "WTOS": {
                "WTO": [schedule.serialize() for schedule in company_weekly_schedules]
            }
        }

        response = self._request("POST", endpoint, request_payload)

        return self._extract_submission_result(response)
