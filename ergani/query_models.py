from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence


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


def _pick_int_value(payload: Dict[str, Any], keys: Sequence[str]) -> Optional[int]:
    value = _pick_value(payload, keys)
    if value is None:
        return None

    if isinstance(value, int):
        return value

    if isinstance(value, float):
        if value.is_integer():
            return int(value)
        raise ValueError(f"Expected EX_BASE_08 integer field, got float: {value!r}")

    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            return None
        try:
            return int(stripped)
        except ValueError as error:
            raise ValueError(
                f"Expected EX_BASE_08 integer field, got: {value!r}"
            ) from error

    raise ValueError(f"Expected EX_BASE_08 integer field, got: {value!r}")


@dataclass(frozen=True)
class CurrentWorkStatusEntry:
    work_slot_start: Optional[str]
    work_slot_end: Optional[str]
    break_minutes: Optional[int]
    break_placement: Optional[str]
    work_type_code: Optional[str]
    extra: Optional[Any] = None
    raw_payload: Optional[Dict[str, Any]] = None

    @classmethod
    def from_payload(cls, payload: Any) -> "CurrentWorkStatusEntry":
        return parse_current_work_status_entry(payload)


def parse_current_work_status_entry(payload: Any) -> CurrentWorkStatusEntry:
    if not isinstance(payload, dict):
        raise ValueError(
            "Expected EX_BASE_08 current work status entry payload to be an object"
        )

    return CurrentWorkStatusEntry(
        work_slot_start=_pick_string_value(
            payload,
            [
                "WorkSlotStart",
                "workSlotStart",
                "WorkStart",
                "workStart",
                "StartTime",
                "startTime",
                "OraApo",
            ],
        ),
        work_slot_end=_pick_string_value(
            payload,
            [
                "WorkSlotEnd",
                "workSlotEnd",
                "WorkEnd",
                "workEnd",
                "EndTime",
                "endTime",
                "OraEos",
            ],
        ),
        break_minutes=_pick_int_value(
            payload,
            [
                "BreakMinutes",
                "breakMinutes",
                "BreakDurationMinutes",
                "breakDurationMinutes",
                "BreakMin",
                "breakMin",
            ],
        ),
        break_placement=_pick_string_value(
            payload,
            [
                "BreakPlacement",
                "breakPlacement",
                "BreakPosition",
                "breakPosition",
                "BreakTimePlacement",
                "breakTimePlacement",
            ],
        ),
        work_type_code=_pick_string_value(
            payload,
            [
                "WorkTypeCode",
                "workTypeCode",
                "TypeCode",
                "typeCode",
                "WorkType",
                "workType",
            ],
        ),
        extra=_pick_value(payload, ["Extra", "extra"]),
        raw_payload=dict(payload),
    )


def parse_current_work_status_entries(payload: Any) -> List[CurrentWorkStatusEntry]:
    if not isinstance(payload, list):
        raise ValueError("EX_BASE_08 response payload must be a list")

    return [parse_current_work_status_entry(entry_payload) for entry_payload in payload]
