from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence

_TRUE_OVERNIGHT_ALIASES = {
    True,
    1,
    "1",
    "true",
    "t",
    "yes",
    "y",
    "on",
}
_FALSE_OVERNIGHT_ALIASES = {
    False,
    0,
    "0",
    "false",
    "f",
    "no",
    "n",
    "",
    "off",
    None,
}


def _pick_value(payload: Dict[str, Any], keys: Sequence[str]) -> Any:
    for key in keys:
        if key in payload:
            return payload[key]

    return None


def _pick_string_value(payload: Dict[str, Any], keys: Sequence[str]) -> Optional[str]:
    value = _pick_value(payload, keys)
    if value is None:
        return None

    return str(value)


def _normalize_overnight_flag(value: Any) -> bool:
    candidate = value
    if isinstance(candidate, str):
        candidate = candidate.strip().lower()

    if candidate in _TRUE_OVERNIGHT_ALIASES:
        return True

    if candidate in _FALSE_OVERNIGHT_ALIASES:
        return False

    raise ValueError(f"Unsupported overnight flag value: {value!r}")


@dataclass(frozen=True)
class ActualWorkLogEntry:
    employee_afm: Optional[str]
    employee_name: Optional[str]
    start_time: Optional[str]
    end_time: Optional[str]
    overnight: bool
    raw_payload: Optional[Dict[str, Any]] = None

    @classmethod
    def from_payload(cls, payload: Any) -> "ActualWorkLogEntry":
        return parse_actual_work_log_entry(payload)


def parse_actual_work_log_entry(payload: Any) -> ActualWorkLogEntry:
    if not isinstance(payload, dict):
        raise ValueError("Expected EX_BASE_07 work log entry payload to be an object")

    return ActualWorkLogEntry(
        employee_afm=_pick_string_value(
            payload,
            ["Afm", "AFM", "EmployeeAfm", "employeeAfm", "employee_afm", "afm"],
        ),
        employee_name=_pick_string_value(
            payload,
            [
                "EmployeeName",
                "employeeName",
                "employee_name",
                "Name",
                "name",
                "FullName",
                "fullName",
            ],
        ),
        start_time=_pick_string_value(
            payload,
            [
                "StartTime",
                "startTime",
                "start_time",
                "TimeFrom",
                "timeFrom",
                "From",
                "from",
            ],
        ),
        end_time=_pick_string_value(
            payload,
            [
                "EndTime",
                "endTime",
                "end_time",
                "TimeTo",
                "timeTo",
                "To",
                "to",
            ],
        ),
        overnight=_normalize_overnight_flag(
            _pick_value(
                payload,
                [
                    "Overnight",
                    "overnight",
                    "OverNight",
                    "IsOvernight",
                    "isOvernight",
                    "CrossesMidnight",
                    "crossesMidnight",
                ],
            )
        ),
        raw_payload=dict(payload),
    )


def parse_actual_work_log_entries(payload: Any) -> List[ActualWorkLogEntry]:
    if not isinstance(payload, list):
        raise ValueError("EX_BASE_07 response payload must be a list")

    return [parse_actual_work_log_entry(entry_payload) for entry_payload in payload]
