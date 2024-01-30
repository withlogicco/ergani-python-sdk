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
)
from ergani.utils import extract_error_message


class ErganiClient:
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

    def submit_work_card(
        self, company_work_cards: List[CompanyWorkCard]
    ) -> Optional[Response]:
        """
        Submits work cards records (check-in, check-out) for employees to the Ergani API
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

        return response

    def submit_overtime(
        self, company_overtimes: List[CompanyOvertime]
    ) -> Optional[Response]:
        """
        Submits overtime records for employees to the Ergani API
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

        return response

    def submit_daily_schedule(
        self, company_daily_schedules: List[CompanyDailySchedule]
    ) -> Optional[Response]:
        """
        Submits schedule records that are updated on a daily basis for employees to the Ergani API
        """

        endpoint = "/Documents/WTODaily"

        request_payload = {
            "WTOS": {
                "WTO": [schedule.serialize() for schedule in company_daily_schedules]
            }
        }

        response = self._request("POST", endpoint, request_payload)

        return response

    def submit_weekly_schedule(
        self, company_weekly_schedules: List[CompanyWeeklySchedule]
    ) -> Optional[Response]:
        """
        Submits weekly schedule records for employees to the Ergani API
        """

        endpoint = "/Documents/WTOWeek"

        request_payload = {
            "WTOS": {
                "WTO": [schedule.serialize() for schedule in company_weekly_schedules]
            }
        }

        response = self._request("POST", endpoint, request_payload)

        return response
