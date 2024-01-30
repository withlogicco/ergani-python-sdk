import json
from datetime import date, datetime, time
from typing import Optional, Union

from requests.models import Response

from ergani.typings import (
    LateDeclarationJustificationType,
    OvertimeJustificationType,
    ScheduleWorkType,
    WorkCardMovementType,
)


def extract_error_message(response: Response) -> str:
    """
    Extracts the error message from a requests Response object.
    """
    content_type: str = response.headers.get("Content-Type", "")

    if "application/json" in content_type:
        try:
            response_data = response.json()
            if "message" in response_data:
                return response_data["message"]
            if "msg" in response_data:
                return response_data["msg"]
            if "detail" in response_data:
                return response_data["detail"]
            if not response_data:
                return ""
            return response_data
        except json.JSONDecodeError:
            pass

    if "text/plain" in content_type:
        return response.text.strip()

    return ""


def format_time(t: time) -> str:
    """
    Formats a datetime.time instance to `HH:MM`
    """
    if not t:
        return ""

    return t.strftime("%H:%M")


def format_date(d: Optional[date]) -> str:
    """
    Formats a datetime.date instance to `dd/nm/YYYY"`
    """
    if not d:
        return ""

    return d.strftime("%d/%m/%Y")


def format_datetime(d: Optional[datetime]) -> str:
    """
    Formats a datetime.datetime instance to an ISO 8601 format
    """
    if not d:
        return ""

    return d.strftime("%Y-%m-%dT%H:%M:%S.%f%z")


def get_day_of_week(d: Optional[date]) -> Union[int, str]:
    """
    Returns the day of the week from a datetime.date instance

    0 - Sunday, 6 - Saturday
    """
    if not d:
        return ""

    day_of_week = d.weekday()
    return (day_of_week + 1) % 7


def get_ergani_workcard_movement_type(movement_type: WorkCardMovementType) -> str:
    movement_type_mapping = {
        "ARRIVAL": "0",
        "DEPARTURE": "1",
    }

    return movement_type_mapping[movement_type]


def get_ergani_late_declaration_justification(
    justification: LateDeclarationJustificationType,
) -> str:
    justification_mapping = {
        "POWER_OUTAGE": "001",
        "EMPLOYER_SYSTEMS_UNAVAILABLE": "002",
        "ERGANI_SYSTEMS_UNAVAILABLE": "003",
    }

    return justification_mapping.get(justification, justification)


def get_ergani_overtime_cancellation(cancellation: bool) -> str:
    return "0" if not cancellation else "1"


def get_ergani_overtime_justification(justification: OvertimeJustificationType) -> str:
    justification_mapping = {
        "ACCIDENT_PREVENTION_OR_DAMAGE_RESTORATION": "001",
        "URGENT_SEASONAL_TASKS": "002",
        "EXCEPTIONAL_WORKLOAD": "003",
        "SUPPLEMENTARY_TASKS": "004",
        "LOST_HOURS_SUDDEN_CAUSES": "005",
        "LOST_HOURS_OFFICIAL_HOLIDAYS": "006",
        "LOST_HOURS_WEATHER_CONDITIONS": "007",
        "EMERGENCY_CLOSURE_DAY": "008",
        "NON_WORKDAY_TASKS": "009",
    }

    return justification_mapping[justification]


def get_ergani_work_type(work_type: ScheduleWorkType) -> str:
    work_type_mapping = {
        "WORK_FROM_OFFICE": "ΕΡΓ",
        "WORK_FROM_HOME": "ΤΗΛ",
        "REST_DAY": "ΑΝ",
        "ABSENT": "ΜΕ",
    }

    return work_type_mapping[work_type]
