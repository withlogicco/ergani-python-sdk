import json
from datetime import date, datetime, time
from urllib.parse import urlsplit, urlunsplit
from typing import Any, List, Optional, Union

from requests.models import Response

from ergani.typings import (
    LateDeclarationJustificationType,
    OvertimeJustificationType,
    ScheduleWorkType,
    WorkCardMovementType,
)


def _normalize_scalar(value: Any) -> str:
    if value is None:
        return ""

    if isinstance(value, str):
        return value.strip()

    return str(value).strip()


def extract_error_message(response: Response) -> str:
    """
    Extracts the error message from a requests Response object

    Args:
        response: A Response object

    Returns:
        The extracted error message
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

    Args:
        t: The time that is going to be formatted

    Returns:
        The formatted time
    """

    if not t:
        return ""

    return t.strftime("%H:%M")


def parse_date(value: Any) -> Optional[date]:
    if value in (None, ""):
        return None

    if isinstance(value, date) and not isinstance(value, datetime):
        return value

    if isinstance(value, datetime):
        return value.date()

    normalized_value = _normalize_scalar(value)
    for date_format in ("%d/%m/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(normalized_value, date_format).date()
        except ValueError:
            continue

    raise ValueError(f"Unsupported date value: {value}")


def parse_datetime(value: Any) -> Optional[datetime]:
    if value in (None, ""):
        return None

    if isinstance(value, datetime):
        return value

    normalized_value = _normalize_scalar(value)
    iso_value = normalized_value.replace("Z", "+00:00")

    try:
        return datetime.fromisoformat(iso_value)
    except ValueError:
        pass

    for datetime_format in (
        "%d/%m/%Y %H:%M",
        "%d/%m/%Y %H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%S.%f%z",
    ):
        try:
            return datetime.strptime(normalized_value, datetime_format)
        except ValueError:
            continue

    raise ValueError(f"Unsupported datetime value: {value}")


def parse_int(value: Any) -> Optional[int]:
    if value in (None, ""):
        return None

    if isinstance(value, bool):
        return int(value)

    if isinstance(value, int):
        return value

    if isinstance(value, float):
        if value.is_integer():
            return int(value)
        raise ValueError(f"Unsupported integer value: {value}")

    normalized_value = _normalize_scalar(value)
    return int(normalized_value)


def parse_bool(value: Any) -> Optional[bool]:
    if value in (None, ""):
        return None

    if isinstance(value, bool):
        return value

    if isinstance(value, int):
        if value in (0, 1):
            return bool(value)
        raise ValueError(f"Unsupported boolean value: {value}")

    normalized_value = _normalize_scalar(value).lower()

    truthy_values = {"1", "true", "yes", "y"}
    falsy_values = {"0", "false", "no", "n"}

    if normalized_value in truthy_values:
        return True

    if normalized_value in falsy_values:
        return False

    raise ValueError(f"Unsupported boolean value: {value}")


def parse_status_code(value: Any) -> Optional[str]:
    if value in (None, ""):
        return None

    if isinstance(value, bool):
        return str(int(value))

    if isinstance(value, float):
        if value.is_integer():
            return str(int(value))
        raise ValueError(f"Unsupported status code value: {value}")

    normalized_value = _normalize_scalar(value)
    return normalized_value or None


def parse_list(value: Any) -> List[Any]:
    if value in (None, ""):
        return []

    if not isinstance(value, list):
        raise ValueError("Expected a list value")

    return value


def format_date(d: Optional[date]) -> str:
    """
    Formats a datetime.date instance to `dd/nm/YYYY"`

    Args:
        d: The date that is going to be formatted

    Returns:
        The formatted date
    """

    if not d:
        return ""

    return d.strftime("%d/%m/%Y")


def format_datetime(d: Optional[datetime]) -> str:
    """
    Formats a datetime.datetime instance to an ISO 8601 format

    Args:
        d: The datetime that is going to be formatted

    Returns:
        The formatted datetime
    """

    if not d:
        return ""

    return d.strftime("%Y-%m-%dT%H:%M:%S.%f%z")


def get_day_of_week(d: Optional[date]) -> Union[int, str]:
    """
    Returns the day of the week from a datetime.date instance

    0 - Sunday, 6 - Saturday

    Args:
        d: The date that is going to be evaluated

    Returns:
        The day of the week
    """

    if not d:
        return ""

    day_of_week = d.weekday()
    return (day_of_week + 1) % 7


def get_ergani_workcard_movement_type(movement_type: WorkCardMovementType) -> str:
    """
    Returns the ergani value for workcard_movement_type

    Args:
        workcard_movement_type: The movement type of a work card

    Returns:
        The Ergani value that is going to be used with the Ergani API
    """

    movement_type_mapping = {
        "ARRIVAL": "0",
        "DEPARTURE": "1",
    }

    return movement_type_mapping[movement_type]


def get_ergani_late_declaration_justification(
    justification: LateDeclarationJustificationType,
) -> str:
    """
    Returns the ergani value for late_declaration_justification

    Args:
        late_declaration_justification: The justification for a late work card submission

    Returns:
        The Ergani value that is going to be used with the Ergani API
    """

    justification_mapping = {
        "POWER_OUTAGE": "001",
        "EMPLOYER_SYSTEMS_UNAVAILABLE": "002",
        "ERGANI_SYSTEMS_UNAVAILABLE": "003",
    }

    return justification_mapping.get(justification, justification)


def get_ergani_overtime_cancellation(cancellation: bool) -> str:
    """
    Returns the ergani value for overtime_cancellation

    Args:
        overtime_cancellation: A value representing if an overtime is going to to be cancelled or not

    Returns:
        The Ergani value that is going to be used with the Ergani API
    """

    return "0" if not cancellation else "1"


def get_ergani_overtime_justification(justification: OvertimeJustificationType) -> str:
    """
    Returns the ergani value for overtime_justification

    Args:
        overtime_justification: The justification of an employee's overtime

    Returns:
        The Ergani value that is going to be used with the Ergani API
    """

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
    """
    Returns the ergani value for work_type

    Args:
        work_type: The work type of an employee's schedule

    Returns:
        The Ergani value that is going to be used with the Ergani API
    """

    work_type_mapping = {
        "WORK_FROM_OFFICE": "ΕΡΓ",
        "WORK_FROM_HOME": "ΤΗΛ",
        "REST_DAY": "ΑΝ",
        "ABSENT": "ΜΕ",
    }

    return work_type_mapping[work_type]
