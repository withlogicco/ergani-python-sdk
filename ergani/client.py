from typing import Any, Dict, List, Optional, Tuple

import requests
from requests.models import Response

from ergani.exceptions import APIError, AuthenticationError
from ergani.utils import extract_error_message

from .auth import ErganiAuthentication


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
        response = requests.request(
            method,
            url,
            json=payload,
            auth=ErganiAuthentication(self.username, self.password, self.base_url),
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
        self,
        employer_tax_identification_number: str,
        business_branch_number: str,
        employee_tax_identification_number: str,
        employee_last_name: str,
        employee_first_name: str,
        work_card_movement_type: str,
        work_card_submission_date: str,
        work_card_movement_datetime: str,
        comments: Optional[str] = "",
        late_declaration_justification_code: Optional[str] = "",
    ) -> Optional[Response]:
        endpoint = "/Documents/WRKCardSE"

        request_payload = {
            "Cards": {
                "Card": [
                    {
                        "f_afm_ergodoti": employer_tax_identification_number,
                        "f_aa": business_branch_number,
                        "f_comments": comments,
                        "Details": {
                            "CardDetails": [
                                {
                                    "f_afm": employee_tax_identification_number,
                                    "f_eponymo": employee_last_name,
                                    "f_onoma": employee_first_name,
                                    "f_type": work_card_movement_type,
                                    "f_reference_date": work_card_submission_date,
                                    "f_date": work_card_movement_datetime,
                                    "f_aitiologia": late_declaration_justification_code,
                                }
                            ]
                        },
                    }
                ]
            }
        }

        response = self._request("POST", endpoint, request_payload)

        return response

    def submit_overtime(
        self,
        business_branch_number: str,
        sepe_service_code: str,
        business_primary_activity_code: str,
        business_branch_activity_code: str,
        kallikratis_municipal_code: str,
        legal_representative_tax_identification_number: str,
        employee_tax_identification_number: str,
        employee_social_security_number: str,
        employee_last_name: str,
        employee_first_name: str,
        overtime_date: str,
        overtime_start_time: str,
        overtime_end_time: str,
        overtime_cancellation: str,
        employee_profession_code: str,
        overtime_justification_code: str,
        weekly_workdays_number: str,
        related_protocol_number: Optional[str] = "",
        related_protocol_date: Optional[str] = "",
        employer_organization: Optional[str] = "",
        business_secondary_activity_code_1: Optional[str] = "",
        business_secondary_activity_code_2: Optional[str] = "",
        business_secondary_activity_code_3: Optional[str] = "",
        business_secondary_activity_code_4: Optional[str] = "",
        comments: Optional[str] = "",
        asee_approval: Optional[str] = "",
    ) -> Tuple[Dict[str, Any], Optional[Response]]:
        endpoint = "/Documents/OvTime"

        request_payload = {
            "Overtimes": {
                "Overtime": [
                    {
                        "f_aa_pararthmatos": business_branch_number,
                        "f_rel_protocol": related_protocol_number,
                        "f_rel_date": related_protocol_date,
                        "f_ypiresia_sepe": sepe_service_code,
                        "f_ergodotikh_organwsh": employer_organization,
                        "f_kad_kyria": business_primary_activity_code,
                        "f_kad_deyt_1": business_secondary_activity_code_1,
                        "f_kad_deyt_2": business_secondary_activity_code_2,
                        "f_kad_deyt_3": business_secondary_activity_code_3,
                        "f_kad_deyt_4": business_secondary_activity_code_4,
                        "f_kad_pararthmatos": business_branch_activity_code,
                        "f_kallikratis_pararthmatos": kallikratis_municipal_code,
                        "f_comments": comments,
                        "f_afm_proswpoy": legal_representative_tax_identification_number,
                        "Ergazomenoi": {
                            "OvertimeErgazomenosDate": [
                                {
                                    "f_afm": employee_tax_identification_number,
                                    "f_amka": employee_social_security_number,
                                    "f_eponymo": employee_last_name,
                                    "f_onoma": employee_first_name,
                                    "f_date": overtime_date,
                                    "f_from": overtime_start_time,
                                    "f_to": overtime_end_time,
                                    "f_cancellation": overtime_cancellation,
                                    "f_step": employee_profession_code,
                                    "f_reason": overtime_justification_code,
                                    "f_weekdates": weekly_workdays_number,
                                    "f_asee": asee_approval,
                                }
                            ]
                        },
                    }
                ]
            }
        }

        response = self._request("POST", endpoint, request_payload)

        return response

    def submit_daily_schedule(
        self,
        business_branch_number: str,
        employee_tax_identification_number: str,
        employee_last_name: str,
        employee_first_name: str,
        schedule_date: str,
        work_type: str,
        workday_start_time: str,
        workday_end_time: str,
        related_protocol_number: Optional[str] = "",
        related_protocol_date: Optional[str] = "",
        comments: Optional[str] = "",
        schedule_start_date: Optional[str] = "",
        schedule_end_date: Optional[str] = "",
    ) -> Tuple[Dict[str, Any], Optional[Response]]:
        endpoint = "/Documents/WTODaily"

        request_payload = {
            "WTOS": {
                "WTO": [
                    {
                        "f_aa_pararthmatos": business_branch_number,
                        "f_rel_protocol": related_protocol_number,
                        "f_rel_date": related_protocol_date,
                        "f_comments": comments,
                        "f_from_date": schedule_start_date,
                        "f_to_date": schedule_end_date,
                        "Ergazomenoi": {
                            "ErgazomenoiWTO": [
                                {
                                    "f_afm": employee_tax_identification_number,
                                    "f_eponymo": employee_last_name,
                                    "f_onoma": employee_first_name,
                                    "f_date": schedule_date,
                                    "ErgazomenosAnalytics": {
                                        "ErgazomenosWTOAnalytics": [
                                            {
                                                "f_type": work_type,
                                                "f_from": workday_start_time,
                                                "f_to": workday_end_time,
                                            }
                                        ]
                                    },
                                }
                            ]
                        },
                    }
                ]
            }
        }

        response = self._request("POST", endpoint, request_payload)

        return response
